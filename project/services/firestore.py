import os
from google.cloud import firestore
from scrapy.utils.serialize import ScrapyJSONEncoder

Collections = {
    'CONFIG': 'scraper_configuration'
}


class Firestore:
    def __init__(self):
        project_id = os.environ.get("PROJECT_ID")
        self.db = firestore.Client(project=project_id)

    # def test(self):
    #     a = self.db.collection('companies').limit(1).get()
    #     print(a[0].to_dict())

    def get_configs(self):
        docs = self.db.collection(Collections['CONFIG']).limit(1).get()
        # docs = self.db.collection(Collections['CONFIG']).get()
        return list(map(lambda doc: doc.to_dict(), docs))
