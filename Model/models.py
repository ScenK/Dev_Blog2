# -*- coding: utf-8 -*-
import datetime
from flask.ext.mongoengine import MongoEngine
from mongoengine import *

db = MongoEngine()

class User(db.Document):
    email        = db.StringField(required=True)
    name         = db.StringField(max_length=50)
    avatar       = db.StringField()
    publish_time = db.DateTimeField(default=datetime.datetime.now, required=True)

class Diary(db.Document):
    title        = db.StringField(required=True)
    content      = db.StringField()
    summary      = db.StringField()
    html         = db.StringField()
    category     = db.StringField(default=u'未分类')
    author       = db.ReferenceField(User)
    tags         = db.ListField(db.StringField())
    comments     = db.ListField(db.EmbeddedDocumentField('Comment'))
    publish_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    update_time  = db.DateTimeField(default=datetime.datetime.now, required=True)

    meta = {'allow_inheritance': True}

class Category(db.Document):
    name         = db.StringField(max_length=120, required=True)
    diaries      = db.ListField(db.ReferenceField(Diary))
    publish_time = db.DateTimeField(default=datetime.datetime.now, required=True)

class Comment(db.EmbeddedDocument):
    content      = db.StringField(required=True)
    name         = db.StringField(max_length=120, required=True)
    email        = db.EmailField()
    publish_time = db.DateTimeField(default=datetime.datetime.now, required=True)

