# Career Site Scraper

## Overview

This is service to scrape job data from a variety of listing urls.

- It is composed in python, using the `scrapy` framework.
- Each crawl employs one of a variety of "spiders," each configured to a particular listing site platform or classification.

## Usage

### Local

Initialization:

1. Install `python3.8` and `pip` (if necessary).
1. Run `python3 -m venv venv` to create a virtual environment folder (within this directory)
1. VSCode setup: "Python: Select Interpreter" > ./venv/bin/python
1. Activate virtual environment: `source venv/bin/activate`
1. Use `pip` to install packages: `pip install -r requirements.txt`

Execution:

```
$ source venv/bin/activate
$ python3 main.test.py
```

### Docker

```sh
$ docker-compose build
$ docker-compose run --rm app python main.test.py
```
