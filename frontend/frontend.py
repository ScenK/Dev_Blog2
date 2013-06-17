# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, abort
from jinja2 import TemplateNotFound
from Model.models import Diary

frontend = Blueprint('frontend', __name__, template_folder='templates', static_folder='static')

@frontend.route('/')
def home():
    diaries = Diary.objects.order_by('-publish_time')
    return render_template('frontend/home.html', diaries=diaries)

@frontend.route('/diary/<diary_id>/<diary_title>')
def diary_detail(diary_id, diary_title=None):
    try:
        diary = Diary.objects(pk=diary_id)[0]
    except:
        abort(404)

    return render_template('frontend/diary/detail.html', diary=diary)
