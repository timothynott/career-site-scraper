import re
import json
from scrapy import Spider, Request
from scrapy.http import JsonRequest
from ..items import JobLoader, WageInfoLoader, ShiftInfoLoader
from ..procs import *

class HydromotionComSpider(Spider):
    name = 'hydromotion.com'
    allowed_domains = ['hydromotion.com', 'jobscore.com', 'jsco.re']
    start_urls = ['https://www.hydromotion.com/about-us/careers/']
    xpath = {
        'job_link': '//h2[text()="Current Job Openings"]/following-sibling::ul//a/@href',
        'title': '//h1[@class="js-title"]//text()',
        'subtitle': '//h2[@class="js-subtitle"]//text()',
        'description': '//div[@id="js-job-description"]//text()',
    }
    re = {
        'city': r'-\s+([^,]+),\s+[A-Z]{2}\s+|\s+[^|]+$',
        'state': r'-\s+[^,]+,\s+([A-Z]{2})\s+|\s+[^|]+$',
    }

    def parse(self, response):
        for job_link in response.xpath(self.xpath['job_link']):
            yield response.follow(job_link, callback=self.parse_job)

    def parse_job(self, response):
        job_loader = JobLoader(response=response)
        job_loader.add_value('company', 'Hydromotion, Inc.')
        job_loader.add_value('jobSourceUrl', response.url)
        title = response.xpath(self.xpath['title']).get()
        job_loader.add_value('title', title)
        job_loader.add_value('jobLevel', title)
        job_loader.add_xpath('city', self.xpath['subtitle'], re=self.re['city'])
        job_loader.add_xpath('state', self.xpath['subtitle'], re=self.re['state'])
        job_loader.add_xpath('jobType', self.xpath['subtitle'])
        job_loader.add_value('jobType', title)
        job_loader.add_xpath('description', self.xpath['description'])
        shift_info_loader = ShiftInfoLoader()
        shift_info_loader.add_value('shifts', title)
        shift_info = shift_info_loader.load_item()
        job_loader.add_value('shiftInfo', shift_info)
        job = job_loader.load_item()
        return job
