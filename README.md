# Career Site Scraper
## Overview
This is service to scrape job data from a variety of listing urls.
* It is composed in python, using the `scrapy` framework.
* Each scrape employs one of a variety of "spiders," each configured to a particular listing site platform or classification.

## Initialization
1. Install `python3.8` and `pip` (if necessary).
1. Run `python3 -m venv venv` to create a virtual environment folder (within this directory)
1. Activate virtual environment: `source venv/bin/activate`
1. Use `pip` to install packages: `pip install -r requirements.txt`

## Usage

1. Activate virtual environment (if you already haven't done so): `source venv/bin/activate`
1. Run a spider as follows (from directory where `scrapy.cfg` is located):
	`scrapy crawl icims -O data.json`


## Other
### Proxy support
Scrapy obeys the following environment variables: `http_proxy`, `https_proxy` and `no_proxy`.

1. To specify proxy to use:

	```sh
	$ export https_proxy=https://user:password@host:port
	```

### Custom settings
Full list of Scrapy settings: https://docs.scrapy.org/en/latest/topics/settings.html

A few examples:

1. Run scrapers in multiple network threads w/o any delays (usually should be used along with proxies):
	```sh
	$ scrapy crawl crosstex.com -O data.json -s CONCURRENT_REQUESTS_PER_DOMAIN=10 -s DOWNLOAD_DELAY=0
	```

2. Turn off HTTP caching:
	```sh
	$ scrapy crawl crosstex.com -O data.json -s HTTPCACHE_ENABLED=False
	```