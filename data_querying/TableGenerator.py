from Mapper import Mapper

class TableGenerator():
    def __init__(self):
        self.mapper = Mapper()
    def generate_table(self, documents_cursor, concept_filter_list):
        columns = []
        documents = []

        for doc in documents_cursor.rewind():
            processed_document = {}
            for key,value in doc.items():
                snomed_ids_of_key = self.mapper.map_to_concept(self.mapper.prepare_fieldname(key))
                for concept_filter in concept_filter_list:
                    if concept_filter in snomed_ids_of_key:
                        columns.append(concept_filter)
                        processed_document[concept_filter] = value
            documents.append(processed_document)
        return list(set(columns)), documents