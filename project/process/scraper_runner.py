import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# TODO: set production value based on memory usage
CONCURRENT_CRAWLS_DEFAULT = 20


class ScraperRunner:
    def __init__(self, config: dict = {}):
        # The path seen from root, ie. from main.py
        settings_file_path = 'project.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.settings = get_project_settings()
        self.process = CrawlerProcess(self.settings)
        self.num_concurrent_crawls = config.get('CONCURRENT_CRAWLS', CONCURRENT_CRAWLS_DEFAULT)

    def run(self, configs: list):
        def crawl_next():
            if not configs:
                return
            config = configs.pop()
            spider_class = config['spider_class']
            d = self.process.crawl(spider_class, config=config)
            # when this crawl completes, crawl_next (to maintain concurrency level)
            d.addCallback(lambda _: crawl_next())

        # initiate crawls
        for _ in range(self.num_concurrent_crawls):
            crawl_next()

        # simultaneously run all processes
        # the script will block here until the crawling is finished
        self.process.start()
