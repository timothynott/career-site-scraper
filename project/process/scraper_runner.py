import os
from project.services.firestore import FirestoreService
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class ScraperRunner:
    def __init__(self):
        # The path seen from root, ie. from main.py
        settings_file_path = 'project.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.settings = get_project_settings()
        self.process = CrawlerProcess(self.settings)
        self.firestore = FirestoreService()

    def run(self, configs):
        # WK: kick off n=20 crawls (configs[:20]), then start one crawl when each finishes
        for config in configs:
            spider_class = config['spider_class']
            self.process.crawl(spider_class, config=config)

        # simultaneously run all processes
        # the script will block here until the crawling is finished
        self.process.start()
