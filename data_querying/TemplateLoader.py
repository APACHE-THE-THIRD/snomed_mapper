from pymongo import MongoClient
import json


class TemplateLoader():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.myCollection

    def get_template(self, template_name):
        template = self.db.TemplateCollection.find_one({"template_name": template_name})
        del template["_id"]
        template_str = json.dumps(template, indent=2)

        return template_str