from pymongo import MongoClient


class DocumentProvider(object):
    """
    provides documents to map form collection
    """
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.myCollection

    def insert_modified_json(self, document):
        self.db.MappedCollection.insert_one(document)

    def insert_json(self, document):
        self.db.InputCappedCollection.insert_one(document)
