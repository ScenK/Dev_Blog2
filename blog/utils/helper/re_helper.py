# -*- coding: utf-8 -*-
import re


class ReHelper(object):

    """ReHelper support muti re functions.

    This helper will support a few muti-used functions for contents that need
    re-place or re-test.
    """

    def __init__(self):
        pass

    def r_slash(self, s):
        """Ensure user submited string not contains '/' or muti '-'.

        Args:
            s: submited string

        Returns:
            replaced slash string
        """
        s = re.sub('[" "\/\--]+', '-', s)
        s = re.sub(r':-', ':', s)
        s = re.sub(r'^-|-$', '', s)

        return s
