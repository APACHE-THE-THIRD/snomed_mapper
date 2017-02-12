from pymongo import MongoClient

class OntologyMongoLoader():

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.myCollection
        self.ontology =self.db.SnomeCollection.find({})
        self.get_ontology_from_mongo()
    def get_ontology(self):
       return self.ontology

    def get_ontology_from_mongo(self):
        self.ontology = self.db.SnomeCollection.find({})

    def find_concepts(self, concept_string):

        result = []
        for concept in self.ontology:
            if concept in concept["term"]:
                result.append(concept)
        return result



