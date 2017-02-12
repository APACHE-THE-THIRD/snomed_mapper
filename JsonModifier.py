
class JsonModifier(object):
    def __init__(self):
        print(" ")

    @staticmethod
    def modify_json(original_document, concept_list, date_time_table):
        original_document["concepts"] = concept_list
        original_document["date"] = date_time_table
        return original_document
