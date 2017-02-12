import Mapper
import DocumentProvider
import tailableCursor
import JsonModifier
import MongoCollectionCreator

class DocumentMapper(object):
    """
    takes documents form documentProvider and maps keys to conceptid's form snomed
    """
    def __init__(self):

        self.provider = DocumentProvider.DocumentProvider()
        self.jsonMod = JsonModifier.JsonModifier()
        self.mngCollCreator = MongoCollectionCreator.MongoCollectionCreator().create_collections()
        self.mapper = Mapper.Mapper()
        tc = tailableCursor.TailableCursor(self).watch_collection_changes()

    def map_document(self, document, date_time_table):
        matching_ids = []
        for key in document:
            mapped_concept = self.mapper.map_to_concept(self.mapper.prepare_fieldname(key))
            if mapped_concept is not None:
                for snomed_id in mapped_concept:
                    matching_ids.append(snomed_id)

        final_json_doc = self.jsonMod.modify_json(document, matching_ids, date_time_table)

        self.provider.insert_modified_json(final_json_doc)