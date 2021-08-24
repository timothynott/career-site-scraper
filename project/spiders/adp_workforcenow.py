import math
import requests
import time
from ._base import CareerSiteSpider
from scrapy import Request
from ..items import JobLoader
from ..procs import *


class ScrapeADPWFNSpider(CareerSiteSpider):
    name = 'adp_workforcenow'
    allowed_domains = ['adp.com']
    custom_settings = {'DOWNLOAD_DELAY': 1}

    num_jobs_per_page = 20

    job_page_url = 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid={}&jobid={}'
    api_base_url = 'https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions'
    api_base_query = '?cid={}&$top=20&$skip={}'
    api_job_path = '/{}?cid={}'

    def start_requests(self):
        # use requests to get url, it will redirect to url with both cid and ccid
        res = requests.get(self.url)
        time.sleep(2)
        # the redirected url with cid and ccid
        standard_url = res.url
        # extract cid
        cid_start_index = standard_url.index('cid=')+4
        cid_len = 36
        cid_end_index = cid_start_index+cid_len
        self.cid = standard_url[cid_start_index:cid_end_index]

        url = self.api_base_url + self.api_base_query.format(self.cid, str(1))
        yield Request(url, callback=self.parse_pagination)

    def parse_pagination(self, response):
        data = response.json()
        assert isinstance(data, dict) and data.get('jobRequisitions'), 'Invalid API payload'

        num_jobs_total = data['meta']['totalNumber']
        num_jobs_per_page = self.num_jobs_per_page
        num_pages = math.ceil(num_jobs_total / num_jobs_per_page)

        # process first page of data
        req_generator = self.parse_listing(response)
        for req in req_generator:
            yield req

        # process second page onwards
        for page in range(1, num_pages):
            url = self.api_base_url + \
                self.api_base_query.format(self.cid, str(1 + (page * num_jobs_per_page)))
            yield Request(url, callback=self.parse_listing)

    def parse_listing(self, response):
        data = response.json()
        assert isinstance(data, dict) and data.get(
            'jobRequisitions'), 'Invalid API payload'
        for job in data['jobRequisitions']:
            job_id = job['customFieldGroup']['stringFields'][0]['stringValue']
            assert job_id, 'No job ID'

            url = self.api_base_url + self.api_job_path.format(job_id, self.cid)
            yield Request(
                url,
                meta={'jobid': job_id},
                callback=self.parse_job
            )

    def parse_job(self, response):
        data = response.json()
        assert isinstance(data, dict), 'No job listing data available'
        job_loader = JobLoader()
        job_loader.add_value('company', self.company_name)
        job_loader.add_value('jobSourceUrl', self.job_page_url.format(
            self.cid, response.meta['jobid']))
        if len(data['requisitionLocations']) == 0:
            self.logger.info('Skipping job because no location data')
            pass
        else:
            job_loader.add_value(
                'city', data['requisitionLocations'][0]['address']['cityName'])
            job_loader.add_value(
                'state', data['requisitionLocations'][0]['address']['countrySubdivisionLevel1']['codeValue'])
            job_loader.add_value(
                'postalCode', data['requisitionLocations'][0]['address']['postalCode'])
        try:
            job_loader.add_value('title', data['requisitionTitle'])
        except:
            self.logger.info('Skipping job because no title')
            pass
        job_loader.add_value('date', data['postDate'])
        job_loader.add_value('description', data['requisitionDescription'])
        try:
            job_loader.add_value('jobType', data['workLevelCode']['shortName'])
        except:
            job_loader.add_value('jobType', '')
        job_loader.add_value('jobLevel', '')
        job = job_loader.load_item()
        return job
