# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import os
from scrapy.item import Item
from scrapy.exceptions import DropItem
from scrapers.cloud_tasks import GoogleCloudTasks


def drop_empty(data):
    for key, val in list(data.items()):
        if isinstance(val, (dict, Item)):
            drop_empty(val)
        elif isinstance(val, list):
            offset = 0
            for n, item in enumerate(val[:]):
                if isinstance(item, (dict, Item)):
                    drop_empty(item)
                if not item:
                    val.pop(n - offset)
                    offset += 1
        if not val and not isinstance(val, (int, float, bool)):
            data.pop(key)


class DropEmptyPipeline:

    def process_item(self, item, spider):
        drop_empty(item)
        if item:
            return item
        else:
            raise DropItem('Empty item')


class IngestJobPipeline:
    queue_name = os.environ.get("JOB_BATCH_INGEST_QUEUE_NAME")
    job_board_ingest_route = "/job-list"

    def open_spider(self, spider):
        self.tasks = GoogleCloudTasks()
        self.current_batch = []

        logging.info("initiating batch {}".format(spider.name))
        # start the batch
        initiate_route = "{}/initiate?source={}".format(
            self.job_board_ingest_route, spider.name)
        self.tasks.queue_task(self.queue_name, initiate_route, {}, 'POST')

    def close_spider(self, spider):
        # send batch to Ingest API
        logging.info("sending batch {}".format(spider.name))
        payload = {
            "source": spider.name,
            "jobs": self.current_batch,
        }
        logging.debug(payload)
        self.tasks.queue_task(
            self.queue_name, self.job_board_ingest_route, payload, 'PUT')

        logging.info("completing batch {}".format(spider.name))
        # complete the batch
        complete_route = "{}/complete?source={}".format(
            self.job_board_ingest_route, spider.name)
        self.tasks.queue_task(self.queue_name, complete_route, {}, 'POST')

        logging.info("done spidering {}...".format(spider.name))

    def process_item(self, item, spider):
        # TODO: implement batch size checking
        # if batch size + item size > max batch size
        #     send current batch to Ingest API
        #     truncate current batch

        normalized_job = {
            "url": item.get('jobSourceUrl'),
            "company": item.get('company'),
            "address": item.get('address'),
            "city": item.get('city'),
            "state": item.get('state'),
            "postalCode": item.get('postalCode'),
            "title": item.get('title'),
            "description": item.get('description'),
            "jobType": item.get('jobType'),
            "jobLevel": item.get('jobLevel'),
            "shiftInfo": item.get('shiftInfo'),
            "wageInfo": item.get('wageInfo'),
        }
        self.current_batch.append(normalized_job)

        return item
