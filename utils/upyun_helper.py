# -*- coding: utf-8 -*-
import datetime
from config import *
from utils.upyun import UpYun
from config import UpyunConfig

class UpYunHelper(object):

    def up_to_upyun(self, collection, data, img_name):

        bucket = UpyunConfig.BUCKET
        admin = UpyunConfig.ADMIN
        password = UpyunConfig.PASSWORD

        u = UpYun(bucket, admin, password)
        u.setApiDomain('v0.api.upyun.com')
        #TODO u.setContentMD5(md5file(data))

        # save file
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        target = '/%s/%s/%s/%s/%s' % (collection, year, month, day, img_name)

        a = u.writeFile(str(target) , data.read(), True)
        url = UpyunConfig.URL + str(target)
        return url
