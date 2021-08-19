from scrapy import Spider


class CareerSitesSpider(Spider):

    def __init__(self, *args, **kwargs):
        super(CareerSitesSpider, self).__init__(*args, **kwargs)

        config = kwargs.get('config')
        self.url = config.url
        self.company_name = config.company_name

    def start_requests(self):
        pass
