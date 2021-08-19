import re
import json
from ._base import CareerSitesSpider
from scrapy import Request
from scrapy.http import JsonRequest
from ..items import JobLoader, WageInfoLoader, ShiftInfoLoader
from ..procs import *


class ScrapeUltiproSpider(CareerSitesSpider):
    name = 'ultipro'
    allowed_domains = ['ultipro.com']

    search_api_path = '/JobBoardView/LoadSearchResults'
    opportunity_path = '/OpportunityDetail?opportunityId={}'

    re = {
        'job_data': r'CandidateOpportunityDetail\((\{.+\})\);\s*',
    }

    # WK: merge all updates/solutions from prototype_scrapy

    def start_requests(self):
        url = self.url

        yield Request(
            url,
            callback=self.parse_pagination
        )

    def parse_pagination(self, response):
        yield JsonRequest(
            response.url + self.search_api_path,
            method='POST',
            data={
                'opportunitySearch': {
                    'Top': 200,
                    'Skip': 0,
                    'QueryString': '',
                    'OrderBy': [
                        {
                            'Value': 'postedDateDesc',
                            'PropertyName': 'PostedDate',
                            'Ascending': False
                        },
                    ],
                },
            },
            meta={'base_url': response.url, },
            callback=self.parse_listing
        )

    def parse_listing(self, response):
        data = response.json()
        assert isinstance(data, dict) and data.get('opportunities'), 'Invalid API payload'
        for opportunity in data['opportunities']:
            opportunity_id = opportunity.get('Id')
            assert opportunity_id, 'No opportunity ID'
            url = response.meta['base_url'] + self.opportunity_path.format(opportunity_id)
            yield Request(
                url,
                meta={
                    'company_name': response.meta['company_name'],
                },
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
                job_loader.add_value('address', address['Line1'])
                job_loader.add_value('city', address['City'])
                job_loader.add_value('state', address['State']['Code'])
                job_loader.add_value('postalCode', address['PostalCode'])
        compensation_amount = data['CompensationAmount']
        if compensation_amount and compensation_amount.get('Value'):
            wage_info_loader = WageInfoLoader()
            wage_info_loader.add_value('base', compensation_amount['Value'])
            wage_info = wage_info_loader.load_item()
            job_loader.add_value('wageInfo', wage_info)
        shift_info_loader = ShiftInfoLoader()
        shift_info_loader.add_value('shifts', data['Title'])
        shift_info = shift_info_loader.load_item()
        job_loader.add_value('shiftInfo', shift_info)
        job = job_loader.load_item()
        return job
