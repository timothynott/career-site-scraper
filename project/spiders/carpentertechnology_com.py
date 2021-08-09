import re
import json
import xml
from urllib.parse import urljoin
from scrapy import Spider, Request
from scrapy.http import JsonRequest
from ..items import JobLoader, WageInfoLoader, ShiftInfoLoader

class CarpentertechnologyComSpider(Spider):
    name = 'carpentertechnology.com'
    allowed_domains = ['carpentertechnology.com', 'myworkdayjobs.com']
    re = {
        'city': r'\b([^,]+),\s+[A-Z]{2}\b',
        'state': r'\b[^,]+,\s+([A-Z]{2})\b',
    }

    def start_requests(self):
        # ? more simple/efficient to use XML request, if can parse response (use xpath?)
        #   but excludes locale (.../en-US/CTCExternal...)
        # ^ XML documentation may be limited to 100 entries, is pagination possible?
        yield JsonRequest('https://cartech.wd5.myworkdayjobs.com/CTCExternal')

    def parse(self, response):
        data = response.json()
        items = data['body']['children'][0]['children'][0]['listItems']
        for item in items:
            url = item['title']['commandLink']
            yield JsonRequest(urljoin(response.url, url), callback=self.parse_job)
        if items:
            # pagination may be broken: may not paginate, may duplicate results
            pos = response.meta.get('pos', 0) + 50
            yield JsonRequest(
                'https://cartech.wd5.myworkdayjobs.com/CTCExternal/fs/searchPagination/%s/%s'
                % (data['ecid'], pos),
                meta={'pos': pos},
            )

    def parse_job(self, response):
        # job_data happens to be in JSONResponse.structuredDataAttributes
        data = json.loads(response.json()['structuredDataAttributes']['data'])
        job_loader = JobLoader()
        job_loader.add_value('company', 'Dynamet, Inc.')
        job_loader.add_value('jobSourceUrl', response.url)
        job_loader.add_value('title', data['title'])
        job_loader.add_value('description', data['description'])
        job_loader.add_value('jobType', data['title'])
        if not job_loader.get_output_value('jobType'):
            job_loader.add_value('jobType', data['employmentType'])
        job_loader.add_value('jobLevel', data['title'])
        location = data['jobLocation']['address']['addressLocality']
        job_loader.add_value('city', location, re=self.re['city'])
        job_loader.add_value('state', location, re=self.re['state'])
        shift_info_loader = ShiftInfoLoader()
        shift_info_loader.add_value('shifts', data['title'])
        shift_info = shift_info_loader.load_item()
        job_loader.add_value('shiftInfo', shift_info)
        job = job_loader.load_item()
        return job
