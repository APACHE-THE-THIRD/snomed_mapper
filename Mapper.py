from pymongo import MongoClient


class Mapper(object):
    """
    maps string from input json document key name to snomedct concept id
    """
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.myCollection


    def map_to_concept(self, fieldName):
        if fieldName not in [("\"_id\""), ("\"title\""), ("\"author\"")]:
            concepts = self.db.SnomedCollection.find({ '$text': { '$search': fieldName } } )
            snomed_ids = self.get_snomed_ids(concepts)
            return snomed_ids
        else:
            return []

    @staticmethod
    def get_snomed_ids(matching_conepts):
        snomed_ids = []
        for concept in matching_conepts:
            snomed_ids.append(concept["conceptid"])
        return snomed_ids

    @staticmethod
    def prepare_fieldname(fieldName):
        prepFieldName = "\"" + fieldName + "\""
        return prepFieldName.lower()

