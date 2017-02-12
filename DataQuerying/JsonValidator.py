import json
from string import whitespace

class JsonValidator():
    @staticmethod
    def validateJson(json_string):

        try:
            json_obj = json.loads(json_string.translate(dict.fromkeys(map(ord, whitespace))))
        except ValueError:
            return False
        return True


