# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
import os
from itemadapter import ItemAdapter
from scrapy.item import Item
from scrapy.exceptions import DropItem
from .services.cloud_tasks import CloudTasksService
from .services.firestore import FirestoreService


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


class WriteJsonPipeline:

    def open_spider(self, spider):
        self.dirname = '_output'
        if not os.path.exists(self.dirname):
            os.mkdir(self.dirname)
        self.filename = '{}/{}_{}.jsonl'.format(self.dirname, spider.name, spider.company_name)
        self.file = open(self.filename, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class IngestPipeline:
    queue_name = os.environ.get("JOB_BATCH_INGEST_QUEUE_NAME")
    job_board_ingest_route = "/ingest"

    def __init__(self):
        self.firestore = FirestoreService()
        self.tasks = CloudTasksService()

    def open_spider(self, spider):
        self.firestore.delete_cached_jobs(spider.url)

    def close_spider(self, spider):
        source = spider.url
        logging.info("creating ingestion task: {}".format(source))
        payload = {"source": source}
        # TODO: restore
        # self.tasks.queue_task(self.queue_name, self.job_board_ingest_route, payload, 'POST')

    def process_item(self, item, spider):
        source = spider.url
        normalized_job = {
            "source": source,
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

        self.firestore.set_cached_job(normalized_job)
        return item
