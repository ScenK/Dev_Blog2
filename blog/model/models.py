# -*- coding: utf-8 -*-
import datetime
from flask.ext.mongoengine import MongoEngine
from mongoengine import *

db = MongoEngine()

class User(db.Document):
    name         = db.StringField(max_length=50, required=True)
    password     = db.StringField()
    email        = db.StringField()
    avatar       = db.StringField()
    signature    = db.StringField() 
    created_at   = db.DateTimeField(default=datetime.datetime.now, required=True)

class Diary(db.Document):
    title        = db.StringField(required=True)
    old_id       = db.IntField()
    content      = db.StringField()
    summary      = db.StringField()
    html         = db.StringField()
    category     = db.StringField(default=u'未分类')
    author       = db.ReferenceField(User)
    tags         = db.SortedListField(db.StringField())
    comments     = db.SortedListField(db.EmbeddedDocumentField('CommentEm'))
    publish_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    update_time  = db.DateTimeField(default=datetime.datetime.now, required=True)

    meta = {'allow_inheritance': True}
    
class Photo(db.Document):
    url          = db.StringField(required=True)     
    title        = db.StringField(required=True)
    album_name   = db.StringField(default=u'未分类')
    description  = db.StringField()
    publish_time = db.DateTimeField(default=datetime.datetime.now, required=True)


class Tag(db.Document):
    name         = db.StringField(max_length=120, required=True)
    diaries      = db.SortedListField(db.ReferenceField(Diary))
    publish_time = db.DateTimeField(default=datetime.datetime.now, required=True)


class Category(db.Document):
    name         = db.StringField(max_length=120, required=True)
    diaries      = db.SortedListField(db.ReferenceField(Diary))
    publish_time = db.DateTimeField(default=datetime.datetime.now, required=True)


class Comment(db.Document):
    content      = db.StringField(required=True)
    author       = db.StringField(max_length=120, required=True)
    email        = db.EmailField()
    diary        = db.ReferenceField(Diary)
    publish_time = db.DateTimeField(default=datetime.datetime.now, required=True)


class Page(db.Document):
    url          = db.StringField(required=True, unique=True)
    title        = db.StringField(required=True)
    content      = db.StringField()
    summary      = db.StringField()
    html         = db.StringField()
    author       = db.ReferenceField(User)
    comments     = db.SortedListField(db.EmbeddedDocumentField('CommentEm'))
    publish_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    update_time  = db.DateTimeField(default=datetime.datetime.now, required=True)

    meta = {'allow_inheritance': True}


class StaticPage(Page):
    pass


class CommentEm(db.EmbeddedDocument):
    content      = db.StringField(required=True)
    author       = db.StringField(max_length=120, required=True)
    email        = db.EmailField()
    publish_time = db.DateTimeField(default=datetime.datetime.now, required=True)
