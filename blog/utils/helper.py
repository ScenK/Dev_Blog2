# -*- coding: utf-8 -*-
import re
import datetime
from HTMLParser import HTMLParser
from utils.upyun import UpYun
from config import UpyunConfig


class MLStripper(HTMLParser):
    """MLStripper support functions for feed Html.

    This helper will help feed contents from Full html tags content to pure
    content.

    Attributes:
        html: Full html tags content
    """
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


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
        s = re.sub('[" "\/\--.]+', '-', s)
        s = re.sub(r':-', ':', s)
        s = re.sub(r'^-|-$', '', s)

        return s


class UpYunHelper(object):
    """UpYunHelper support methods to upload images to upyun.

    This helper will help upload images to upyun site to get forign links.
    """
    def __init__(self):
        pass

    def up_to_upyun(self, collection, data, img_name):
        """Method to upload single image to upyun.

        Args:
            collection: string collection name
            data: image file data
            img_name: string image name, not hashed before

        Return:
            url: like 'http://v0.api.upyun.com/collection1/2013/07/01/abc.jpg'
        """
        bucket = UpyunConfig.BUCKET
        admin = UpyunConfig.ADMIN
        password = UpyunConfig.PASSWORD

        u = UpYun(bucket, admin, password)
        u.setApiDomain('v0.api.upyun.com')
        # TODO u.setContentMD5(md5file(data))

        # save file
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        target = '/%s/%s/%s/%s/%s' % (collection, year, month, day, img_name)

        u.writeFile(str(target), data.read(), True)
        url = UpyunConfig.URL + str(target)
        return url


class SiteHelpers(object):
    """Site Helper.

    This helper will support several functions.
    """
    def __init__(self):
        pass

    def strip_html_tags(self, html):
        s = MLStripper()
        s.feed(html)

        return s.get_data()

    def secure_filename(self, name):
        h = ReHelper()
        s = h.r_slash(name)

        return s.lower()

    def up_to_upyun(self, collection, data, img_name):
        u = UpYunHelper()
        url = u.up_to_upyun(collection, data, img_name)

        return url
