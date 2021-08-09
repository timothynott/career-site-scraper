README
======


Installation
------------

* Install ``Python3.8`` and ``pip`` first.

1. Then install scrapers:

.. code:: shell

	$ pip install -U -r requirements.txt


Usage
------

1. Change the current directory (where `scrapy.cfg` located):

.. code:: shell

	$ cd scrapers

2. Run scraper for a given website and save all data into a specified JSON file:

.. code:: shell

	$ scrapy crawl crosstex.com -O data.json


Proxy support
-------------

Scrapy obeys the following environment variables: `http_proxy`, `https_proxy` and `no_proxy`.

1. To specify proxy to use:

.. code:: shell

	$ export https_proxy=https://user:password@host:port


Custom settings
---------------

Full list of Scrapy settings: https://docs.scrapy.org/en/latest/topics/settings.html

A few examples:

1. Run scrapers in multiple network threads w/o any delays (usually should be used along with proxies):

.. code:: shell

	$ scrapy crawl crosstex.com -O data.json -s CONCURRENT_REQUESTS_PER_DOMAIN=10 -s DOWNLOAD_DELAY=0

2. Turn off HTTP caching:

.. code:: shell

	$ scrapy crawl crosstex.com -O data.json -s HTTPCACHE_ENABLED=False
