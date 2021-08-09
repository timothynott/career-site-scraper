import re
import json
from scrapy import Spider, Request
from scrapy.http import JsonRequest
from ..items import JobLoader, WageInfoLoader, ShiftInfoLoader
from ..procs import *


class CrosstexComSpider(Spider):
    name = 'crosstex.com'
    allowed_domains = ['icims.com']
    # use '.../search?pr=1' for pagination instead of duplicating request?
    #   would it be possible to derive this strategy automatically?
    start_urls = ['https://jobs-cantelmedical.icims.com/jobs/search?ss=1']
    xpath = {
        'listing_link': '//div[contains(@class, "iCIMS_PagingBatch")]//a/@href',
        # could just use iCIMS_Anchor, but best to be explicit in cases of potential generic
        'job_link': '//div[contains(@class, "iCIMS_JobsTable")]/div//a[@class="iCIMS_Anchor"]/@href',
        'title': '//h1[@class="iCIMS_Header"]//text()',
        'location': '//span[text()="Location"]/following-sibling::span/text()',
        'description': (
            '//h2[contains(text(), "Who we are")]/preceding-sibling::'
            'div[contains(@class, "iCIMS_InfoMsg_Job")]//text()'
        ),
    }
    re = {
        'city': r'\bUS-[A-Z]{2}-([A-Za-z -]+)\b',
        'state': r'\bUS-([A-Z]{2})-[A-Za-z -]+\b',
    }

    def parse(self, response):
        # again, is this an unnecessarily duplicated request?
        # why in_iframe? is present in pagination hrefs, not in subsequent rendered page url (==response.url?)
        #   if in_iframe excluded, job data is not present in response HTML doc
        yield Request(response.url + '&in_iframe=1', callback=self.parse_pagination)

    # ? listing links appear to render for first five pages only
    #   may be more stable to use "next page" button,
    #       or just to see pattern '/search?pr=(1,2,3,4,...)'
    #           if pr=(>max), simply returns no results
    def parse_pagination(self, response):
        # note .xpath() NOT .xpath().get()
        for link in response.xpath(self.xpath['listing_link']):
            # https://docs.scrapy.org/en/latest/topics/request-response.html#scrapy.http.TextResponse.follow
            # > response.follow(various*) versus Request(absolute url only)
            #       *absolute url, relative url, Link object, Selector object
            yield response.follow(link, callback=self.parse_listing)

    def parse_listing(self, response):
        for link in response.xpath(self.xpath['job_link']):
            yield response.follow(link, callback=self.parse_job)

    def parse_job(self, response):
        # why is response passed here (and not in others)?
        job_loader = JobLoader(response=response)
        job_loader.add_value('company', 'Crosstex International, Inc.')
        job_loader.add_value('jobSourceUrl', response.url)
        title = response.xpath(self.xpath['title']).get()
        job_loader.add_value('title', title)
        job_loader.add_value('jobLevel', title)
        job_loader.add_value('jobType', title)
        job_loader.add_xpath('city', self.xpath['location'], re=self.re['city'])
        job_loader.add_xpath('state', self.xpath['location'], re=self.re['state'])
        job_loader.add_xpath('description', self.xpath['description'])
        shift_info_loader = ShiftInfoLoader()
        shift_info_loader.add_value('shifts', title)
        shift_info = shift_info_loader.load_item()
        job_loader.add_value('shiftInfo', shift_info)
        job = job_loader.load_item()
        return job
