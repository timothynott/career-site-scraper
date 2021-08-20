import os
from google.cloud import firestore
from scrapy.utils.serialize import ScrapyJSONEncoder

Collections = {
    'CONFIG': 'scraper_configuration',
    'JOB_CACHE': 'job_cache'
}


class Firestore:
    def __init__(self):
        project_id = os.environ.get("PROJECT_ID")
        self.db = firestore.Client(project=project_id)

    def get_configs(self):
        docs = self.db.collection(Collections['CONFIG']).get()
        return list(map(lambda doc: doc.to_dict(), docs))

    def set_cached_job(self, doc: dict):
        return self.db.collection(Collections['JOB_CACHE']).add(doc)

    def delete_cached_jobs(self, source: str):
        collection_ref = self.db.collection(Collections['JOB_CACHE'])
        # WK: ensure where clause functional
        jobs_for_source = collection_ref.where('source', '==', source).select({}).get()
        for job in jobs_for_source:
            collection_ref.document(job.id).delete()
