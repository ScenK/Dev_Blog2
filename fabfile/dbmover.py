# -*- coding: utf-8 -*-

from fabric.api import *
from pymongo import Connection
from mongoengine import *
from werkzeug.security import generate_password_hash
from Model.models import *

class DbMover(object):
    def __init__(self):
        self.sourse_db = Connection().dev_blog


    def connect_db(self):
        #sourse_db = raw_input('Type your sourse database (from where?) :')
        #if sourse_db:
            #print 'OK!'
        target_db = raw_input('Type your target database (to where?) :')
        if target_db:
            self.target_db = target_db
            connect(target_db)
            print 'connect DB: OK!'


    def move_user(self):
        print 'Start moving User Data...'

        """sourse_db"""
        accounts = self.sourse_db.accounts
        admin = self.sourse_db.admins.find_one()
        profile = accounts.find_one()

        """target_db"""
        user = User(name=admin.get('user'))
        user.password = generate_password_hash(password=admin.get('password'))
        user.avatar = profile.get('avatar')
        user.signature = profile.get('desc')
        user.created_at = profile.get('site_start')
        user.save(validate=False)

        print 'User Data moved OK!'

    def move_diary(self):
        print 'Start moving Diary Data...'

        """sourse_db"""
        diaries = self.sourse_db.diaries.find()

        author = User.objects.first()

        """target_db"""
        for d in diaries:
            diary = Diary(title=d.get('title'))
            diary.old_id = int(d.get('_id'))
            diary.content = d.get('content')
            diary.summary = d.get('summary')
            diary.html = d.get('html')
            diary.category = d.get('category')
            diary.author = author
            diary.tags = d.get('tags')
            diary.publish_time = d.get('publish_time')
            diary.update_time = d.get('update_time')
            diary.save(validate=False)

        print 'Diary Data moved OK!'


    def move_comment(self):
        print 'Start moving Comment Data...'

        """sourse_db"""
        comments = self.sourse_db.comments.find()

        author = User.objects.first()

        """target_db"""
        for c in comments:
            diary = Diary.objects(old_id=int(c.get('did')))

            #save in Comment
            comment = Comment(content=c.get('content'))
            comment.author = c.get('user')
            comment.email = c.get('email')
            comment.diary = diary[0]
            comment.publish_time = c.get('publish_time')
            comment.save(validate=False)

            #save in CommentEm
            commentEm = CommentEm(
                        author = c.get('user'),
                        content = c.get('content'),
                        email = c.get('email'),
                        publish_time = c.get('publish_time')
                    )
            diary.update_one(push__comments=commentEm)

        print 'Comment Data moved OK!'


    def move_category(self):
        print 'Start moving Category Data...'

        """sourse_db"""
        categories = self.sourse_db.categories.find()

        """target_db"""
        for c in categories:
            category = Category(name=c.get('name'))
            category.publish_time = c.get('publish_time')
            category.save(validate=False)

            for d in c.get('diaries'):
                diary = Diary.objects(old_id=int(d.get('did'))).first()
                Category.objects(name=c.get('name')).update_one(push__diaries=diary)

        print 'Category Data moved OK!'


    def main(self):
        self.connect_db()
        self.move_user()
        self.move_diary()
        self.move_comment()
        self.move_category()
