# -*- coding: utf-8 -*-
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask.ext.login import (current_user, login_required,
                            login_user, logout_user, UserMixin,
                            confirm_login, fresh_login_required)
from jinja2 import TemplateNotFound
from Model.models import Diary, CommentEm, Category, Comment
from Model.models import User as UserModel
import markdown

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active

@admin.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST' and 'username' in request.form:
        user = UserModel.objects.first()
        username = request.form["username"]
        password = request.form["password"]
        
        if username == user.name and check_password_hash(user.password, password):
            if login_user(User(user.name, user.pk)):
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
    categories = Category.objects.all()
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

        a, cat = Category.objects.get_or_create(name=category, defaults={'diaries': [post]})
        if not cat:
            Category.objects(name=category).update_one(push__diaries=post)
        return redirect(url_for("admin.diary_list"))

    return render_template('admin/diary/add.html', error=error, categories=categories)

@admin.route('/diary/edit/<diary_id>', methods=['GET', 'POST'])
@login_required
def diary_edit(diary_id=None):
    error = None
    diary = Diary.objects.get_or_404(pk=diary_id)[0]

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

    return render_template('admin/diary/edit.html', error=error, diary=diary)

@admin.route('/diary/list')
@login_required
def diary_list():
    diaries = Diary.objects.order_by('-publish_time')
    return render_template('admin/diary/list.html', diaries=diaries)

@admin.route('/diary/del/<diary_id>')
@login_required
def diary_del(diary_id):
    Diary.objects.get_or_404(pk=diary_id).delete()
    return redirect(url_for("admin.diary_list"))

@admin.route('/category/list')
@login_required
def category_list():
    categories = Category.objects.order_by('-publish_time')
    return render_template('admin/category/list.html', categories=categories)

@admin.route('/category/del/<category_name>')
@login_required
def category_del(category_name):
    Category.objects.get_or_404(name=category_name).delete()
    return redirect(url_for("admin.category_list"))

@admin.route('/comment/list')
@login_required
def comment_list():
    comments = Comment.objects.order_by('-publish_time')
    return render_template('admin/comment/list.html', comments=comments)

@admin.route('/comment/reply', methods=['POST'])
#@login_required
def comment_reply():
    if request.method == 'POST':
        author = request.form['author']
        did = request.form['did']
        title = request.form['title']
        email = request.form['email']
        content = request.form['content']

        post = Diary.objects(pk=did)
        commentEm = CommentEm(
                    author = current_user.name,
                    content = content,
                )
        post.update_one(push__comments=commentEm)

        ''' Save in Comment Model for admin manage'''
        comment = Comment(content=content)
        comment.diary = post[0]
        comment.author = current_user.name
        comment.save(validate=False)
    return ''

@admin.route('/account/settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    return render_template('admin/account/settings.html')
