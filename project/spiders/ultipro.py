import re
import json
from scrapy import Spider, Request
from scrapy.http import JsonRequest
from ..items import JobLoader, WageInfoLoader, ShiftInfoLoader
from ..procs import *


class UltiProSpider(Spider):
    name = 'ultipro'
    allowed_domains = ['ultipro.com']
    start_urls = ['https://recruiting.ultipro.com/ARC1018']
    re = {
        'job_data': r'CandidateOpportunityDetail\((\{.+\})\);\s*',
    }
    search_api_endpoint = '/JobBoardView/LoadSearchResults'
    opportunity_url = '/OpportunityDetail?opportunityId={}'

    # make paginated request to API (JSON)
    def parse(self, response):
        yield JsonRequest(
            response.url + self.search_api_endpoint,
            method='POST',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            data={
                'opportunitySearch': {
                    'Top': 100,
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
            meta={'base_url': response.url},
            callback=self.careers_api_call,
        )

    # get listing urls
    # make request to each listing url (HTML)
    def careers_api_call(self, response):
        data = response.json()
        assert isinstance(data, dict) and data.get('opportunities'), 'Invalid API payload'
        for opportunity in data['opportunities']:
            opportunity_id = opportunity.get('Id')
            assert opportunity_id, 'No opportunity ID'
            url = response.meta['base_url'] + \
                self.opportunity_url.format(opportunity_id)
            yield Request(url, callback=self.parse_job)

    def parse_job(self, response):
        # data happens to be in HTML script function, parse to JSON dict
        # > var opportunity = new US.Opportunity.CandidateOpportunityDetail({ _job_data_ })
        match = re.search(self.re['job_data'], response.text)
        assert match, 'No job data on the page'
        data = json.loads(match.group(1))
        job_loader = JobLoader()
        job_loader.add_value('company', 'Creative Converting, Inc.')
        job_loader.add_value('jobSourceUrl', response.url)
        job_loader.add_value('title', data['Title'])
        job_loader.add_value('description', data['Description'])
        job_loader.add_value('jobType', data['Title'])
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
