# -*- coding: utf-8 -*-

import urllib
from fabric.api import *
from mongoengine import *
from Model.models import Diary
from config import *

connect(Config.MONGODB_SETTINGS.get('DB'))

class Redirector(object):

    def __init__(self):
        """Init sourse database.
        You should change it with your real name.
        """
        pass

    def main(self):
        try:
            local("rm redirect_map.conf")
        except:
            pass

        local("touch redirect_map.conf")

        diaries = Diary.objects.all()

        file_object = open('redirect_map.conf', 'w')

        for diary in diaries:
            record = self.generate_single_line(diary)
            file_object.write(record)

        print 'config file generate done!'
        file_object.close()

    def generate_single_line(self, diary):
        try:
            old_id = diary.old_id
            object_id = diary.pk
            diary_title = urllib.quote(diary.title.encode('utf-8'))

            record = 'rewrite ^/diary/detail/' + str(old_id) + ' ' + str(Config.SITE_URL) +'/diary/' + str(object_id) + '/' + diary_title + ' permanent;' + '\n'

            return record
        except Exception as e:
            print str(e)
