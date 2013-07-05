# -*- coding: utf-8 -*-
from config import *
from utils.upyun import UpYun

class UpYunHelper(object):

    def up_to_upyun(collection, data):
        img_data = data.get('body')
        img_name = data.get('filename').encode("utf-8")

        bucket = conf['upyun_bucket']
        admin = conf['upyun_admin']
        password = conf['upyun_password']

        u = UpYun(bucket, admin, password)
        u.setApiDomain('v0.api.upyun.com')
        #TODO u.setContentMD5(md5file(data))

        # save file
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        target = '/%s/%s/%s/%s/%s' % (collection, year, month, day, img_name)
        a = u.writeFile(str(target) , img_data, True)
        url = conf['upyun_url'] + str(target)
        return url
