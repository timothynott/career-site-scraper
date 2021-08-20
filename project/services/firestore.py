import os
from google.cloud import firestore

Collections = {
    'CONFIG': 'scraper_configuration',
    'JOB_CACHE': 'job_cache'
}


# TODO: make service singleton
class FirestoreService:
    def __init__(self):
        project_id = os.environ.get("PROJECT_ID")
        self.db = firestore.Client(project=project_id)

    def get_configs(self):
        docs = self.db.collection(Collections['CONFIG']).get()
        return list(map(lambda doc: doc.to_dict(), docs))

    # WK: set/delete docs more in parallel?
    def set_cached_job(self, doc: dict):
        collection_ref = self.db.collection(Collections['JOB_CACHE'])
        return collection_ref.add(doc)

    def delete_cached_jobs(self, source: str):
        collection_ref = self.db.collection(Collections['JOB_CACHE'])
        docs = collection_ref.where('source', '==', source).select({}).get()
        for doc in docs:
            collection_ref.document(doc.id).delete()
