from pymongo import MongoClient


class OntologyLoader(object):
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.myCollection
        self.ontology =[]

    def load_ontology_to_mongo(self):
        with open("resources\desc_full.txt", encoding='utf-8') as infile:
            for line in infile:
                tab = line.split('\t')
                self.ontology.append(
                    {"id": tab[0],
                     "conceptid": tab[4],
                     "term": tab[7].lower()
                     }
                )
        self.db.SnomedCollection.insert_many(self.ontology)
        return True
