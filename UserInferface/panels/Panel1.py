import wx
import wx.adv

from data_querying.DateConverter import DateConverter
from data_querying.DocumentProvider import DocumentProvider
from data_querying.TableGenerator import TableGenerator


class DataQueryPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.doc_provider = DocumentProvider()
        self.tab_gen = TableGenerator()

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.VERTICAL)
        hbox3 = wx.BoxSizer(wx.VERTICAL)
        hbox4 = wx.BoxSizer(wx.VERTICAL)
        hbox5 = wx.BoxSizer(wx.VERTICAL)
        fgs = wx.FlexGridSizer(3, 4, 10, 10)

        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.date_static_box = wx.StaticBox(self, -1, "Date options")
        self.sbox_sizer = wx.StaticBoxSizer(self.date_static_box, wx.VERTICAL)
        self.low_date_lbl = wx.StaticText(self, -1, "After:  ")
        self.upp_date_lbl = wx.StaticText(self, -1, " Before:  ")
        self.low_bnd_date_picker = wx.adv.DatePickerCtrl(self, style = wx.BORDER_SUNKEN)
        self.upp_bnd_date_picker = wx.adv.DatePickerCtrl(self)
        self.low_bnd_date_picker.Bind(wx.adv.EVT_DATE_CHANGED, self.on_date_filter_change)
        self.upp_bnd_date_picker.Bind(wx.adv.EVT_DATE_CHANGED, self.on_date_filter_change)

        self.box.AddMany([self.low_date_lbl, self.low_bnd_date_picker, self.upp_date_lbl,  self.upp_bnd_date_picker])
        self.sbox_sizer.Add(self.box, 0 , wx.ALL | wx.CENTER, 10)

        self.search_concept_ctrl = wx.SearchCtrl(self, size=(300,25))

        self.search_concept_ctrl.Bind(wx.EVT_TEXT, self.on_cocept_search)

        self.concept_listView = wx.ListCtrl(self, size=(300, 400), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.concept_listView.InsertColumn(0, "Term            ")
        self.concept_listView.InsertColumn(1, "SNOMED ID")
        self.concept_listView.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_concept_listview_selection)


        self.documents_label = wx.StaticText(self, -1, "Filtered documents", (20, 20))
        self.document_listView = wx.ListCtrl(self, size=(300, 405), style = wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.document_listView.InsertColumn(0, "Title")
        self.document_listView.InsertColumn(1, "Author")
        self.document_listView.InsertColumn(2, "Date")
        self.document_listView.InsertColumn(3, "id")
        self.document_listView.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_document_selection)

        self.label = wx.StaticText(self, -1, "Selected concept filters", (20,20))
        self.filter_listView = wx.ListCtrl(self, size=(300, 339), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.filter_listView.InsertColumn(0, "Term")
        self.filter_listView.InsertColumn(1, "SNOMED ID")
        self.filter_list = []
        self.filter_listView.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_filter_listview_selection)

        self.table_label = wx.StaticText(self, -1, "Document table", (20, 20))
        self.table_listview = wx.ListCtrl(self, size=(300, 405), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.filtered_documents = []

        hbox2.AddMany([ (self.search_concept_ctrl), (self.concept_listView) ])
        hbox3.AddMany([ (self.documents_label), (self.document_listView) ])
        hbox4.AddMany([ (self.sbox_sizer), (self.label), (self.filter_listView) ])
        hbox5.AddMany([(self.table_label) ,(self.table_listview)])

        fgs.AddMany([(hbox2), (hbox4), (hbox3), (hbox5)])
        hbox.Add(fgs)
        self.SetSizer(hbox)
        self.date_converter = DateConverter()
        self.init_gui()

    def init_gui(self):
        self.search_concept_ctrl.SetDescriptiveText("Search in concepts")
        self.low_bnd_date_picker.SetValue(wx.DateTime(1,0,2017))
        self.upp_bnd_date_picker.SetValue(wx.DateTime(14,1,2017))


    def on_cocept_search(self, event):
        string_filter = event.GetString()
        if len(string_filter) > 2:
            self.update_concept_view(string_filter)

    def update_concept_view(self, string_filter):
        self.concept_listView.DeleteAllItems()
        concepts = self.doc_provider.find_concepts(string_filter)
        for concept in concepts:
            self.concept_listView.Append([ concept["term"], concept["conceptid"]])

    def on_text_search(self, event):
        self.update_docs_view()

    def update_docs_view(self):
        dates_list = self.get_dates()
        self.document_listView.DeleteAllItems()
        self.filtered_documents = self.doc_provider.query_date_concepts(self.filter_list, dates_list)


        for doc in self.filtered_documents:
            self.document_listView.Append([doc["title"], doc["author"],
                                           doc["date"],
                                           doc["_id"]
                                           ])
        self.generate_table(self.filtered_documents.rewind())


    def generate_table(self, documents_cursor):
        self.table_listview.ClearAll()
        columns, documents = self.tab_gen.generate_table(documents_cursor, self.filter_list)

        for i,column in enumerate(columns):
            self.table_listview.InsertColumn(i, column)

        for  i, document in enumerate(documents):
            self.table_listview.InsertItem(i, str(""))
            for key,val in document.items():
                if key in columns:
                    self.table_listview.SetItem(i, columns.index(key), str(val))

    def on_date_filter_change(self, event):
        self.update_docs_view()


    def on_concept_listview_selection(self, event):

        selected_item_index = event.GetEventObject().GetFocusedItem()
        selected_item_snomed_id = self.concept_listView.GetItem(selected_item_index, col = 1).GetText()
        selected_item_term = self.concept_listView.GetItem(selected_item_index, col = 0).GetText()
        self.filter_listView.Append([selected_item_term, selected_item_snomed_id])
        self.filter_list.append(selected_item_snomed_id)

        self.update_docs_view()

    def on_filter_listview_selection(self, event):

        selected_item_index = event.GetEventObject().GetFocusedItem()
        selected_item = self.filter_listView.GetItem(selected_item_index, col=1).GetText()
        self.filter_listView.DeleteItem(selected_item_index)
        self.filter_list.remove(selected_item)

        self.update_docs_view()

    def on_document_selection(self, event):
        document_view_index = event.GetEventObject().GetFocusedItem()
        selected_item_mongoid = self.document_listView.GetItem(document_view_index, col=3).GetText()
        doc = self.doc_provider.get_document_by_id(selected_item_mongoid)

        self.new = NewWindow(parent=None, id=-1, document_to_display=doc)
        self.new.Show()

    def get_dates(self):
        upper_bound = self.low_bnd_date_picker.GetValue()
        lower_bound = self.upp_bnd_date_picker.GetValue()

        upper_bound_datetime = self.date_converter.wxdate2datetime(upper_bound)
        lower_bound_datetime = self.date_converter.wxdate2datetime(lower_bound)

        dates = [lower_bound_datetime, upper_bound_datetime]

        return dates

class NewWindow(wx.Frame):

    def __init__(self, parent, id, document_to_display):
        wx.Frame.__init__(self, parent, id, 'Document view', size=(400, 300))

        self.concept_listView = wx.ListCtrl(self, size=(300, 400), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        values = []
        for index, key in enumerate(document_to_display):
            self.concept_listView.InsertColumn(index, key)
            values.append(document_to_display[key])

        self.concept_listView.Append(values)
        wx.Frame.CenterOnScreen(self)