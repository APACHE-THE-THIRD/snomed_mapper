import wx
from data_querying.JsonValidator import JsonValidator
from DocumentProvider import DocumentProvider
from data_querying.TemplateLoader import TemplateLoader
import json


class JsonInsertionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.doc_provider = DocumentProvider()
        self.template_loader = TemplateLoader()
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(3, 3, 10, 10)

        hbox2 = wx.BoxSizer(wx.VERTICAL)
        hbox3 = wx.BoxSizer(wx.VERTICAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)

        self.text_field_desc = wx.StaticText(self, -1, "Insert document:", (20, 20))
        self.template_listview_desc = wx.StaticText(self, -1, "Choose template:", (20, 20))
        self.text_field = wx.TextCtrl(self, size=(250, 350), style=wx.TE_RICH2 | wx.TE_MULTILINE | wx.TE_PROCESS_TAB)
        self.validate_bttn = wx.Button(self, label="Validate JSON")
        self.save_json_bttn = wx.Button(self, label="Save document")

        self.teamplate_listview = wx.ListCtrl(self, size=(250, 350), style=wx.LC_REPORT | wx.BORDER_SUNKEN)

        hbox4.AddMany([(self.validate_bttn), (self.save_json_bttn)])
        hbox2.AddMany([(self.text_field_desc), (self.text_field), (hbox4)])
        hbox3.AddMany([(self.template_listview_desc), (self.teamplate_listview)])
        fgs.AddMany([(hbox2), (hbox3)])
        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)

        hbox.Add(fgs, proportion = 2, flag = wx.ALL | wx.EXPAND, border = 15)
        self.SetSizer(hbox)

        self.validator = JsonValidator()
        self.init_gui()

    def init_gui(self):
        self.teamplate_listview.InsertColumn(0, "Template name")
        self.teamplate_listview.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_template_listview_selection)
        self.Bind(wx.EVT_BUTTON, self.on_validate_bttn, self.validate_bttn)
        self.Bind(wx.EVT_BUTTON, self.on_save_bttn, self.save_json_bttn)
        self.text_field.SetValue("{\n\t"
                                 "\"title\":\"tytul\","
                                 "\n\t"
                                 "\"author\":\"autor\""
                                 "\n}")
        self.fill_template_listview()
    def fill_template_listview(self):
        self.teamplate_listview.Append(["template1"])


    def on_validate_bttn(self, event):
        self.text_field_desc.SetLabelText("Validation")
        content = self.text_field.GetValue()
        if self.validator.validateJson(content):
            mssg = wx.MessageBox("correct json", "JSON validation")
        else:
            mssg = wx.MessageBox("Incorrect json syntax", "JSON validation")

    def on_save_bttn(self, event):
        self.text_field_desc.SetLabelText("Saving")

        content = self.text_field.GetValue()
        if self.validator.validateJson(content):
            self.doc_provider.insert_json(json.loads(content))
            mssg = wx.MessageBox("Document succesfuly added", "JSON validation")
            self.text_field.SetValue("")
        else:
            mssg = wx.MessageBox("Incorrect json syntax", "JSON validation")

    def on_template_listview_selection(self, event):
        selected_item_index = event.GetEventObject().GetFocusedItem()
        selected_item = self.teamplate_listview.GetItem(selected_item_index, col=0).GetText()
        print(selected_item)
        template = self.template_loader.get_template(selected_item)
        self.text_field.SetValue(template)