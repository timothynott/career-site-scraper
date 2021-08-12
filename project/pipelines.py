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
from .services.cloud_tasks import GoogleCloudTasks


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

            
            
class WriteJsonPipeline:

    def open_spider(self, spider):
        self.dirname = '_output'
        if not os.path.exists(self.dirname):
            os.mkdir(self.dirname)
        self.filename = self.dirname + '/' + spider.config['company_name'] + '_' + spider.name + '.json'
        self.file = open(self.filename, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class DropEmptyPipeline:

    def process_item(self, item, spider):
        drop_empty(item)
        if item:
            return item
        else:
            raise DropItem('Empty item')


class IngestPipeline:
    queue_name = os.environ.get("JOB_BATCH_INGEST_QUEUE_NAME")
    job_board_ingest_route = "/job-list"

    def open_spider(self, spider):
        self.tasks = GoogleCloudTasks()
        self.current_batch = []

        # TODO: Use source/site name, not spider name.
        logging.info("{}: initiating ingestion".format(spider.name))
        # task: initiate ingestion
        initiate_route = "{}/initiate?source={}".format(
            self.job_board_ingest_route, spider.name)
        self.tasks.queue_task(self.queue_name, initiate_route, {}, 'POST')

    def close_spider(self, spider):
        # task: send jobs
        logging.info("{}: sending job batch".format(spider.name))
        payload = {
            "source": spider.name,
            "jobs": self.current_batch,
        }
        logging.debug(payload)
        self.tasks.queue_task(
            self.queue_name, self.job_board_ingest_route, payload, 'PUT')

        logging.info("{}: completing ingestion".format(spider.name))
        # task: complete ingestion
        complete_route = "{}/complete?source={}".format(
            self.job_board_ingest_route, spider.name)
        self.tasks.queue_task(self.queue_name, complete_route, {}, 'POST')

        logging.info("{}: closing spider".format(spider.name))

    def process_item(self, item, spider):
        # TODO: implement batching based on size
        # if batch size + item size > max batch size (1 MB)
        #     truncate batch and send to IngestAPI

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
