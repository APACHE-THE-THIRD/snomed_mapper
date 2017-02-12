from pymongo import MongoClient, CursorType
import time
from dateGenerator import DateGenerator

class TailableCursor(object):

    def __init__(self, docMapperRef):
        self.document_mapper = docMapperRef
        self.date_gen = DateGenerator()

    def watch_collection_changes(self):

        client = MongoClient()
        db = client.myCollection

        inputCollection = db.InputCappedCollection

        inputCollection.insert({"title": "tytul", "author": "autor"})

        cursor = inputCollection.find({}, cursor_type = CursorType.TAILABLE_AWAIT)
        while cursor.alive:
            try:
                new_document = cursor.next()
                self.document_mapper.map_document(new_document, self.date_gen.get_current_date())

            except StopIteration:
                time.sleep(0.1)



