import json
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# WK: create config class
all_configs = [
    {
        'url': 'https://jobs-cantelmedical.icims.com/jobs/search?ss=1',
        'company_name': 'Cantel Medical',
        'spider_class': 'icims',
    },
    {
        'url': 'https://external-weatherford.icims.com/jobs/search?ss=1&searchRelation=keyword_all',
        'company_name': 'Weatherford',
        'spider_class': 'icims'
    },
    {
        'url': 'https://globalcareers-entegrisinc.icims.com/jobs/search?ss=1',
        'company_name': 'Entegris, Inc.',
        'spider_class': 'icims'
    },
    {
        'url': 'https://globalhub-berryglobal.icims.com/jobs/search?ss=1',
        'company_name': 'Berry Global Inc.',
        'spider_class': 'icims'
    },
    {
        'url': 'https://recruiting2.ultipro.com/AMS1003AMSII',
        'company_name': 'Amsted Industries',
        'spider_class': 'ultipro'
    },
    {
        'url': 'https://recruiting.ultipro.com/ARC1018',
        'company_name': 'ARCH',
        'spider_class': 'ultipro'
    },
    {
        'url': 'https://recruiting.ultipro.com/PRO1027PROMA',
        'company_name': 'ProMach',
        'spider_class': 'ultipro'
    },
    {
        'url': 'https://recruiting.ultipro.com/COM1037COMAR',
        'company_name': 'Comar',
        'spider_class': 'ultipro'
    },
]

configs = all_configs[:1]


class ScraperRunner:
    def __init__(self):
        # The path seen from root, ie. from main.py
        settings_file_path = 'project.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.settings = get_project_settings()
        self.process = CrawlerProcess(self.settings)

    def run(self):
        for config in configs:
            spider_class = config['spider_class']
            self.process.crawl(spider_class, config=config)

        # simultaneously run all processes
        # the script will block here until the crawling is finished
        self.process.start()
