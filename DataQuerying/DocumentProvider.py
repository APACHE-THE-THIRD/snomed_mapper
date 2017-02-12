from bson import ObjectId
from pymongo import MongoClient


class DocumentProvider:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.myCollection
        self.mapped_collection = self.db["MappedCollection"]


    def query_date_concepts(self, concepts_filter_table, dates_list):
        retrieved_data = self.db.MappedCollection.find({'$and':
                                                            [
                                                                {'concepts':
                                                                    {'$in' :
                                                                      concepts_filter_table
                                                                    }
                                                                 },
                                                                { 'date' : {'$lte': dates_list[0], '$gte': dates_list[1] } }
                                                            ]
                                                        })
        return retrieved_data


    def find_concepts(self, concept_filter):
        filt =  "\"" + concept_filter + "\""
        retrieved_data = self.db.SnomedCollection.find({'$text': {'$search': filt}})
        return retrieved_data

    def get_document_by_id(self, id):
        obj_id = "ObjectId(\"" + id + "\")"
        document = self.db.MappedCollection.find_one({ "_id": ObjectId(id)})
        print(document)
        return document