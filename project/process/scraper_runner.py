import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class ScraperRunner:
    def __init__(self):
        # The path seen from root, ie. from main.py
        settings_file_path = 'project.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.settings = get_project_settings()
        self.process = CrawlerProcess(self.settings)

    def run(self):
        self.process.crawl('icims')

        # the script will block here until the crawling is finished
        self.process.start()
