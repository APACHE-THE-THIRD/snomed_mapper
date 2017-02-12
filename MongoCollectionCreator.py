import pymongo
from pymongo import MongoClient
from OntologyLoader import OntologyLoader

class MongoCollectionCreator(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.myCollection

        self.ontology_collection_name = "SnomedCollection"
        self.input_collection_name = "InputCappedCollection"
        self.output_collection_name = "MappedCollection"
        self.collection_list = self.db.collection_names()
        self.loader = OntologyLoader()


    def create_collections(self):
        self.create_coll_load_data(self.ontology_collection_name, remove_data = False, loading_method = self.loader.load_ontology_to_mongo)
        self.create_capped_collection(self.input_collection_name)

        self.create_collection(self.output_collection_name, remove_data= False)
        self.create_text_index(self.output_collection_name)
        self.create_text_idex(self.ontology_collection_name)

    def create_collection(self, collection_name, remove_data):
        if(collection_name in self.collection_list):
            print(collection_name + " exists")
            if remove_data:
                    self.db[collection_name].delete_many({})
        else:
            self.db.create_collection(collection_name)

    def create_coll_load_data(self, collection_name, remove_data, loading_method):
        if (collection_name in self.collection_list):
            print(collection_name + " exists")
            if remove_data:
                self.db[collection_name].delete_many({})
        else:
            self.db.create_collection(collection_name)

        if self.db[collection_name].find({}).count() == 0:
            result = loading_method()

    def create_capped_collection(self, collection_name):
        if(collection_name in self.collection_list):
            self.db[collection_name].drop()

        self.db.create_collection(collection_name, capped=True, size=10 * 1000000)  # x * megabytes


    def create_text_idex(self, collection_name):
        self.db[collection_name].create_index([('term', pymongo.TEXT)], name='search_index',
                                              default_language='english')
    def create_text_index(self, collection_name):
        self.db[collection_name].create_index([('title', pymongo.TEXT), ('author', pymongo.TEXT)], name='search_title_index',
                                              default_language='english')


    def ontology_loader(self):
        return self.loader