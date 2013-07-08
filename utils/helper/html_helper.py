# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.html = ''

    def handle_data(self, data):
        self.html += data
