import re
import json
from ._base import CareerSiteSpider
from scrapy import Request
from ..items import JobLoader, ShiftInfoLoader
from ..procs import *


class IcimsSpider(CareerSiteSpider):
    name = 'icims'
    allowed_domains = ['icims.com']

    xpath = {
        'listing_link': '//div[contains(@class, "iCIMS_PagingBatch")]//a/@href',
        'job_link': '//div[contains(@class, "iCIMS_JobsTable")]/div//a[@class="iCIMS_Anchor"]/@href',
    }
    re = {
        'job_page_script_json': r"<script type=\"application/ld\+json\">({?(.+)\"hiringOrganization\":.+)</script>",
    }

    def start_requests(self):
        url = self.url + '&in_iframe=1'
        yield Request(url, callback=self.parse_pagination)

    def parse_pagination(self, response):
        for link in response.xpath(self.xpath['listing_link']):
            yield response.follow(link, callback=self.parse_listing)

    def parse_listing(self, response):
        for link in response.xpath(self.xpath['job_link']):
            yield response.follow(link, callback=self.parse_job)

    def parse_job(self, response):
        match = re.search(self.re['job_page_script_json'], response.text)
        assert match, 'No job data here'
        data = json.loads(match.group(1))
        # pass job if description is unavailable or address state is unavailable
        if data['description'] == 'UNAVAILABLE' or data['jobLocation'][0]['address']['addressRegion'] == 'UNAVAILABLE':
            pass
        else:
            job_loader = JobLoader(response=response)
            job_loader.add_value('company', self.company_name)
            job_loader.add_value('jobSourceUrl', response.url)
            title = data['title']
            job_loader.add_value('title', title)
            job_loader.add_value('jobLevel', title)
            job_loader.add_value('jobType', title)
            job_loader.add_value('city', data['jobLocation']
                                 [0]['address']['addressLocality'])
            job_loader.add_value(
                'state', data['jobLocation'][0]['address']['addressRegion'])
            job_loader.add_value(
                'postalCode', data['jobLocation'][0]['address']['postalCode'])
            job_loader.add_value(
                'address', data['jobLocation'][0]['address']['streetAddress'])
            job_loader.add_value('description', data['description'])
            job_loader.add_value('date', data['datePosted'])
            job = job_loader.load_item()
            return job
