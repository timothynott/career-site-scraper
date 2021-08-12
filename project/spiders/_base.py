from scrapy import Spider

class CareerSitesSpider(Spider):

    def __init__(self, *args, **kwargs):
        super(CareerSitesSpider, self).__init__(*args, **kwargs)
        self.config = kwargs.get('config')

    def start_requests(self):
        pass