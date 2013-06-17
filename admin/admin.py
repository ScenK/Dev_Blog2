# -*- coding: utf-8 -*-
from functools import wraps
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask.ext.login import (current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from jinja2 import TemplateNotFound
from Model.models import User, Diary, Comment
import markdown

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active


class Anonymous(AnonymousUser):
    name = u"Anonymous"

USERS = {
    1: User(u"Notch", 1),
    2: User(u"Steve", 2),
    3: User(u"Creeper", 3, False),
}

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())

@admin.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST' and 'username' in request.form:
        username = request.form["username"]
        if username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(USER_NAMES[username], remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index.index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template('admin/login.html', error=error)

@admin.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("admin.index"))

@admin.route('/')
@login_required
def index():
    return render_template('admin/dashboard.html')

@admin.route('/diary/add', methods=['GET', 'POST'])
@login_required
def diary_add():
    error = None
    if request.method == 'POST' and 'title' and 'content' in request.form:
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]
        tags = request.form["tags"]


        post = Diary(title=title)
        post.content = content
        post.summary = markdown.markdown(content[0:80] + '...')
        post.html = markdown.markdown(content)
        post.tags = tags.split(',')
        post.save()
        return redirect(url_for("admin.index"))

    return render_template('admin/Diary/add.html', error=error)

@admin.route('/diary/edit', methods=['GET', 'POST'])
@login_required
def diary_edit():
    error = None
    if request.method == 'POST' and 'title' and 'content' in request.form:
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]
        tags = request.form["tags"]


        post = Diary(title=title)
        post.content = content
        post.summary = markdown.markdown(content[0:80] + '...')
        post.html = markdown.markdown(content)
        post.tags = tags.split(',')
        post.save()
        return redirect(url_for("admin.index"))

    return render_template('admin/Diary/add.html', error=error)

@admin.route('/diary/list')
@login_required
def diary_list():
    diaries = Diary.objects.all()
    return render_template('admin/Diary/list.html', diaries=diaries)

@admin.route('/diary/del/<diary_id>')
@login_required
def diary_del(diary_id):
    message=None
    Diary.objects(pk=diary_id).delete()
    return redirect(url_for("admin.index"))
