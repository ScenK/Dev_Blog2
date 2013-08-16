# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    """MyHTMLParser support functions for feed Html.

    This helper will help feed contents from Full html tags content to pure
    content.

    Attributes:
        html: Full html tags content
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.html = ''

    def handle_data(self, data):
        self.html += data
