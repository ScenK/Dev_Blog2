# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request, url_for
from jinja2 import TemplateNotFound
from Model.models import Diary, Category, CommentEm, Comment
from config import *
import PyRSS2Gen
import datetime
from utils.email_util import send_reply_mail

frontend = Blueprint('frontend', __name__, template_folder='templates', static_folder='static')


@frontend.route('/')
def home():
    diaries = Diary.objects.order_by('-publish_time')
    categories = Category.objects.order_by('-publish_time')

    return render_template('frontend/home.html', diaries=diaries, categories=categories)


@frontend.route('/diary/<diary_id>/<diary_title>')
def diary_detail(diary_id, diary_title=None):
    diary = Diary.objects(pk=diary_id)[0]
    categories = Category.objects.order_by('-publish_time')

    guest_name = request.cookies.get('guest_name') 
    guest_email = request.cookies.get('guest_email')
    
    return render_template('frontend/diary/detail.html', diary=diary, categories=categories,
                           guest_name=guest_name, guest_email=guest_email)


@frontend.route('/diary/list/<page_num>')
def diary_list(page_num):
    next_page = False
    diary_num = len(Diary.objects)
    categories = Category.objects.order_by('-publish_time')

    diaries = Diary.objects.order_by('-publish_time')[int(page_num):int(page_num)+5] 

    if diary_num > int(page_num)+5:
        next_page = True

    return render_template('frontend/diary/list.html', diaries=diaries, categories=categories,
                           next_page=next_page, page_num=page_num)



@frontend.route('/category/<category_name>')
def category_list(category_name):
    categories = Category.objects.order_by('-publish_time')
    diaries = Diary.objects(category=category_name).order_by('-publish_time')
    return render_template('frontend/category/list.html', category=category_name,
                           diaries=diaries, categories=categories)


@frontend.route('/comment/add', methods=['POST'])
def comment_add():
    if request.method == 'POST':
        name = request.form['username']
        did = request.form['did']
        email = request.form['email']
        content = request.form['comment']

        post = Diary.objects(pk=did)
        diary_title = post[0].title

        commentEm = CommentEm(
                    author = name,
                    content = content,
                    email = email
                )
        post.update_one(push__comments=commentEm)

        ''' Save in Comment Model for admin manage'''
        comment = Comment(content=content)
        comment.diary = post[0]
        comment.email = email
        comment.author = name
        comment.save(validate=False)

        try:
            send_reply_mail(Config.EMAIL, Config.MAIN_TITLE + u'收到了新的评论, 请查收',
                            content, did, name, diary_title)
            return 'success'
        except Exception as e:
            return str(e)


@frontend.route('/feed')
def rss():
    articles = Diary.objects[:12]
    items = []
    for article in articles:
        content = article.html

        url = Config.SITE_URL + '/diary/detail/' + str(article.pk) + '/' + article.title
        items.append(PyRSS2Gen.RSSItem(
            title = article.title,
            link = url,
            description = content,
            guid = PyRSS2Gen.Guid(url),
            pubDate = article.publish_time,
        ))
    rss = PyRSS2Gen.RSS2(
        title = Config.MAIN_TITLE,
        link = Config.SITE_URL,
        description = Config.DESCRIPTION,
        lastBuildDate = datetime.datetime.now(),
        items = items
    ).to_xml()
    return rss
