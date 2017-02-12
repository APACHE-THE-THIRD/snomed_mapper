from datetime import datetime


class DateGenerator():

    @staticmethod
    def get_current_date():
        now = datetime.now()
        return now