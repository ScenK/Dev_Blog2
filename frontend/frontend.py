# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request, url_for
from jinja2 import TemplateNotFound
from Model.models import Diary, Category, Comment

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

    return render_template('frontend/diary/detail.html', diary=diary, categories=categories)

@frontend.route('/category/<category_name>')
def category_list(category_name):
    categories = Category.objects.order_by('-publish_time')
    diaries = Diary.objects(category=category_name).order_by('-publish_time')
    return render_template('frontend/category/list.html', category=category_name, diaries=diaries, categories=categories)

@frontend.route('/comment/add', methods=['POST'])
def comment_add():
    if request.method == 'POST':
        name = request.form['username']
        did = request.form['did']
        email = request.form['email']
        comment = request.form['comment']

        post = Diary.objects(pk=did)
        comment = Comment(
                    author = name,
                    content = comment,
                    email = email
                )
        post.update_one(push__comments=comment)
        return '' 
