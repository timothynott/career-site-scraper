import math
import json
import re
from ._base import CareerSiteSpider
from scrapy import Request
from scrapy.http import JsonRequest
from ..items import JobLoader, WageInfoLoader, ShiftInfoLoader
from ..procs import *


class UltiproSpider(CareerSiteSpider):
    name = 'ultipro'
    allowed_domains = ['ultipro.com']

    api_search_path = '/JobBoardView/LoadSearchResults'
    opportunity_path = '/OpportunityDetail?opportunityId={}'

    re = {
        'job_data': r'CandidateOpportunityDetail\((\{.+\})\);\s*',
    }

    num_jobs_per_page = 200

    def build_search_request_body(self, page: int):
        jobs_per_page = self.num_jobs_per_page
        return {
            'opportunitySearch': {
                'Top': jobs_per_page,
                'Skip': jobs_per_page * page,
                'QueryString': '',
                'OrderBy': [
                    {
                        'Value': 'postedDateDesc',
                        'PropertyName': 'PostedDate',
                        'Ascending': False
                    },
                ],
            },
        }

    def start_requests(self):
        yield Request(self.url, callback=self.parse_main)

    def parse_main(self, response):
        yield JsonRequest(
            response.url + self.api_search_path,
            method='POST',
            data=self.build_search_request_body(page=0),
            meta={'base_url': response.url},
            callback=self.parse_pagination
        )

    def parse_pagination(self, response):
        data = response.json()
        assert isinstance(data, dict) and data.get(
            'totalCount'), 'Invalid API payload'

        num_jobs_total = data['totalCount']
        num_jobs_per_page = self.num_jobs_per_page
        num_pages = math.ceil(num_jobs_total / num_jobs_per_page)

        # parse first page of results (this response)
        req_generator = self.parse_listing(response)
        for req in req_generator:
            yield req

        # parse other pages of results
        for page in range(1, num_pages):
            yield JsonRequest(
                response.url,
                method='POST',
                data=self.build_search_request_body(page),
                meta={'base_url': response.meta['base_url']},
                callback=self.parse_listing
            )

    def parse_listing(self, response):
        data = response.json()
        assert isinstance(data, dict) and data.get(
            'opportunities'), 'Invalid API payload'
        for opportunity in data['opportunities']:
            opportunity_id = opportunity.get('Id')
            assert opportunity_id, 'No opportunity ID'
            url = response.meta['base_url'] + \
                self.opportunity_path.format(opportunity_id)
            yield Request(
                url,
                callback=self.parse_job
            )

    def parse_job(self, response):
        match = re.search(self.re['job_data'], response.text)
        assert match, 'No job data on the page'
        data = json.loads(match.group(1))
        job_loader = JobLoader()
        # TODO: change company name to actually have company name
        job_loader.add_value('company', self.company_name)
        job_loader.add_value('jobSourceUrl', response.url)
        job_loader.add_value('title', data['Title'])
        job_loader.add_value('description', data['Description'])
        job_loader.add_value('jobType', data['Title'])
        job_loader.add_value('date', data['PostedDate'])
        if not job_loader.get_output_value('jobType') and data['FullTime']:
            job_loader.add_value('jobType', 'FULL_TIME')
        job_loader.add_value('jobLevel', data['Title'])
        if data['Locations']:
            location = data['Locations'][0]
            address = location['Address']
            if address['Country']['Code'] == 'USA':
                try:
                    job_loader.add_value('address', address['Line1'])
                    job_loader.add_value('city', address['City'])
                    job_loader.add_value('state', address['State']['Code'])
                    job_loader.add_value('postalCode', address['PostalCode'])
                except:
                    self.logger.warning('location data is null, skip')
                    return
        compensation_amount = data['CompensationAmount']
        if compensation_amount and compensation_amount.get('Value'):
            wage_info_loader = WageInfoLoader()
            wage_info_loader.add_value('base', compensation_amount['Value'])
            wage_info = wage_info_loader.load_item()
            job_loader.add_value('wageInfo', wage_info)
        job = job_loader.load_item()
        return job
