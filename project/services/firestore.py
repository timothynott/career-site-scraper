import os
from google.cloud import firestore
from scrapy.utils.serialize import ScrapyJSONEncoder

# WK: crutch
os.environ.setdefault("PROJECT_ID", "ff-app-dev")


class Firestore:
    def __init__(self):
        project_id = os.environ.get("PROJECT_ID")
        self.db = firestore.Client(project=project_id)

    def test(self):
        a = self.db.collection('companies').limit(1).get()
        print(a[0].to_dict())
