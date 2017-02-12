from DocumentMapper import  DocumentMapper
import threading


class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    @staticmethod
    def start_thread():
        docMapper = DocumentMapper()

    def run(self):
        self.start_thread()
