from wx import DateTime
import datetime
class DateConverter():
    """
    from now timestamp(generated by date picker) to dictionary
    """
    @staticmethod
    def wxdate2datetime(wxdate):
        if wxdate.IsValid():
            ymd = map(int, wxdate.FormatISODate().split('-'))
            date = datetime.datetime(*ymd)
            return date
        else:
            return None

    @staticmethod
    def dict_date2string(dictionary_date):
        str_date = str(dictionary_date["day"]) +"."+ str(dictionary_date["month"]) +"." +str(dictionary_date["year"])
        return str_date