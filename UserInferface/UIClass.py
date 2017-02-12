import wx
import App

from UserInferface.panels.Panel1 import DataQueryPanel
from UserInferface.panels.Panel2 import JsonInsertionPanel



class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="App")
        self.services = App.App().start()

        hbox = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        notebook = wx.Notebook(self)

        data_query_panel = DataQueryPanel(notebook)
        json_insertion_panel = JsonInsertionPanel(notebook)
        notebook.AddPage(json_insertion_panel, "Json Panel")
        notebook.AddPage(data_query_panel, "Data Query Panel")

        sizer.Add(notebook)
        self.SetSizerAndFit(sizer)

if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()

