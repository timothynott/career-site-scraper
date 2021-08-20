from scrapy import Spider


class CareerSiteSpider(Spider):

    def __init__(self, *args, **kwargs):
        super(CareerSiteSpider, self).__init__(*args, **kwargs)

        config = kwargs.get('config')

        self.url = config['url']
        self.company_name = config['company_name']

    def start_requests(self):
        pass
