# -*- coding: utf-8 -*-
import json
import re
from werkzeug import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask.ext.login import (current_user, login_required,
                            login_user, logout_user, UserMixin)
from jinja2 import TemplateNotFound

from model.models import (Diary, Category, Comment, Tag, Photo, StaticPage,
                          CommentEm)
from model.models import User as UserModel
from tasks.email_tasks import send_email_task
from utils.helper.html_helper import MyHTMLParser
from utils.helper.upyun_helper import UpYunHelper
from utils.helper.re_helper import ReHelper

admin = Blueprint('admin', __name__, template_folder='templates',
                  static_folder='static')

class User(UserMixin):
    """ User object for Flasklogin

    define name, id, and active for Flasklogin use
    """
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active


@admin.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for user to auth.

    use Flasklogin Class login_user() to login user.

    Methods:
        GET and POST

    Args:
        GET:
            none
        POST:
            username: string
            password: string

    Returns:
        GET:
            none
        POST:
            none
    """
    error = None
    if request.method == 'POST' and 'username' in request.form:
        user = UserModel.objects.first()
        username = request.form["username"]
        password = request.form["password"]

        if username == user.name and check_password_hash(user.password,
                                                         password):
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
    """Action for logout current_user.

    call this method for logout current_user.
    """
    logout_user()
    flash("Logged out.")
    return redirect(url_for("admin.index"))


@admin.route('/')
@login_required
def index():
    """Page for dashboard.

    only display static page.
    """

    return render_template('admin/dashboard.html')


@admin.route('/diary/edit/<diary_id>', methods=['GET', 'POST'])
@login_required
def diary_edit(diary_id=None):
    """ Edit diary from admin

    receives title, content(html), tags and cagetory
    save title, content(html), pure content(further use), tags and cagetory
    also auto save author as current_user.

    this method will auto save new Category or Tag if not exist otherwise save
    in existed none with push only diary_object

    Args:
        diary_id: diary_id
        title: string
        html: string
        cagetory: string
        tags: list

    Save:
        title: string
        html: string
        content: string without html tags
        category: string
        tags: list
        summary: first 80 characters in content with 3 dots in the end
        author: current_user_object
    """
    if request.method == 'POST' and 'title' and 'content' in request.form:
        re_helper = ReHelper()

        title = re_helper.r_slash(request.form["title"])
        html = request.form["content"]
        category = re_helper.r_slash(request.form["category"])
        tags = request.form["tags"]

        ''' save simple data for further use'''
        parser = MyHTMLParser()
        parser.feed(html)
        content = parser.html # the pure content without html tags

        splited_tags = tags.split(',')

        author = UserModel.objects.first()

        try:
            diary = Diary.objects(pk=diary_id).first()
        except:
            diary = Diary(title=title)

        old_cat = diary.category
        old_tags = diary.tags

        diary.title = title
        diary.content = content
        diary.category = category
        diary.summary = content[0:80] + '...'
        diary.html = html
        diary.author = author
        diary.tags = splited_tags
        diary.save()

        a, cat = Category.objects.get_or_create(name=category,
                                                defaults={'diaries': [diary]})
        if not cat:
            Category.objects(name=category).update_one(push__diaries=diary)
            if old_cat is not None:
                Category.objects(name=old_cat).update_one(pull__diaries=diary)

        for t in old_tags:
            Tag.objects(name=t).update_one(pull__diaries=diary)

        for i in splited_tags:
            b, tag = Tag.objects.get_or_create(name=i,
                                               defaults={'diaries': [diary]})
            if not tag:
                Tag.objects(name=i).update_one(push__diaries=diary)

        return redirect(url_for("admin.diary_list"))

    else:
        try:
            diary = Diary.objects(pk=diary_id).first()
        except:
            diary = None
        categories = Category.objects.all()

        return render_template('admin/diary/edit.html', diary=diary,
                               categories=categories)


@admin.route('/diary/list')
@login_required
def diary_list():
    """Admin Diary lit page.

    show all diaries.

    Methods:
        GET

    Args:
        none

    Returns:
        Diary object
    """
    diaries = Diary.objects.order_by('-publish_time')
    return render_template('admin/diary/list.html', diaries=diaries)


@admin.route('/diary/del/<diary_id>')
@login_required
def diary_del(diary_id):
    """Admin Diary Delete Action

    Used for delete Diary.Also del reference Tag and Category.

    Methods:
        GET

    Args:
        diary_id: diary ObjectID

    Returns:
        none
    """
    diary = Diary.objects(pk=diary_id)
    Category.objects(name=diary[0].category).update_one(pull__diaries=diary[0])
    diary.delete()
    return redirect(url_for("admin.diary_list"))


@admin.route('/category/list')
@login_required
def category_list():
    """Admin Category lit page.

    show all categories.

    Methods:
        GET

    Args:
        none

    Returns:
        Category object
    """
    categories = Category.objects.order_by('-publish_time')
    return render_template('admin/category/list.html', categories=categories)


@admin.route('/category/del/<category_name>')
@login_required
def category_del(category_name):
    """Admin Category Delete Action

    Used for delete Category.

    Methods:
        GET

    Args:
        category_name: string

    Returns:
        none
    """
    Category.objects.get_or_404(name=category_name).delete()
    return redirect(url_for("admin.category_list"))


@admin.route('/comment/del/<comment_id>')
@login_required
def comment_del(comment_id):
    """Admin Comment Delete Action

    Used for delete Comment.Del comment from DiaryCommentEm and CommentDB

    Methods:
        GET

    Args:
        comment_id: CommentObjectedID

    Returns:
        none
    """
    comment = Comment.objects.get_or_404(pk=comment_id)

    diary = Diary.objects(pk=comment.diary.pk)

    diary.update_one(pull__comments={'content': comment.content})

    comment.delete()

    return redirect(url_for("admin.comment_list"))


@admin.route('/comment/list')
@login_required
def comment_list():
    """Admin Comments list page.

    Used for list all comments.

    Methods:
        GET

    Args:
        none

    Returns:
        comments object
    """
    comments = Comment.objects.order_by('-publish_time')
    return render_template('admin/comment/list.html', comments=comments)


@admin.route('/comment/reply', methods=['POST'])
@login_required
def comment_reply():
    """Comment Reply Action.

    Used for reply guests comment and send notification email.

    Methods:
        POST

    Args:
        author: guest_name
        did: diaryObjectID
        title: diary_title
        email: guest_email
        content: reply content

    Returns:
        status: {success: true/false , reason: Exception}
    """
    if request.method == 'POST':
        author = request.form['author']
        did = request.form['did']
        title = request.form['title']
        email = request.form['email']
        content = request.form['content']

        post = Diary.objects(pk=did)
        commentEm = CommentEm(
                    author = u'博主回复',
                    content = content,
                )
        post.update_one(push__comments=commentEm)

        ''' Save in Comment model for admin manage'''
        comment = Comment(content=content)
        comment.diary = post[0]
        comment.author = current_user.name
        comment.save(validate=False)

        try:
            send_email_task(email, u'您评论的文章《' + title + u'》收到了来自\
                            博主的回复, 请查收', content, did, author, title)
            return json.dumps({'success': 'true'})
        except Exception as e:
            return json.dumps({'success': 'false', 'reason': str(e)})


@admin.route('/account/settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    """Account Settings Page.

    allow admin to change profile.

    Methods:
        GET and POST

    Args:
        GET:
            none

        POST:
            username: string
            pass1   : password
            pass2   : password twice for validate
            signature: user profile signature
            email   : for get reply email notification

    Returns:
        GET:
            user object
        POST:
            none
    """
    user = UserModel.objects(name=current_user.name).first()
    if request.method == 'POST':
        username = request.form['username']
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']
        signature = request.form['signature']
        email = request.form['email']
        avatar = request.form['avatar']

        if pass1 and pass2 and pass1 == pass2:
            user.password = generate_password_hash(password=pass1)

        if username:
            user.name = username

        if signature:
            user.signature = signature

        if email:
            user.email = email

        if avatar:
            user.avatar = avatar

        user.save()

        if pass1 or username:
            logout_user()
            flash(u"请重新登陆")
            return redirect(url_for("admin.index"))

        return redirect(url_for("admin.account_settings"))
    else:
        return render_template('admin/account/settings.html', user=user)


@admin.route('/account/settings/upload_avatar', methods=['POST'])
@login_required
def account_upload_avatar():
    """Admin Account Upload Avatar Action.

    *for Ajax only.

    Methods:
        POST

    Args:
        files: [name: 'userfile']

    Returns:
        status: {success: true/false}
    """
    if request.method == 'POST':
        data = request.files['userfile']
        filename = secure_filename(data.filename)
        helper = UpYunHelper()
        url = helper.up_to_upyun('account', data, filename)
        if url:
          return json.dumps({'success': 'true', 'url': url})
        else:
          return json.dumps({'success': 'false'})


@admin.route('/diary/add-photo', methods=['POST'])
@login_required
def diary_add_photo():
    """Admin Diary Add Photo Action.

    *for Ajax only.

    Methods:
        POST

    Args:
        files: [name: 'userfile']

    Returns:
        status: {success: true/false}
    """
    if request.method == 'POST':
        data = request.files['userfile']
        filename = secure_filename(data.filename)
        helper = UpYunHelper()
        url = helper.up_to_upyun('diary', data, filename)
        if url:
          return json.dumps({'success': 'true', 'url': url})
        else:
          return json.dumps({'success': 'false'})


@admin.route('/album/detail/<album_name>', methods=['GET', 'POST'])
@login_required
def album_detail(album_name):
    """Album Detail Admin Page.

    Used for upload new photos to UpYun and set deail about album.Also, if
    the album index is not set, use the first photo.

    Methods:
        GET and POST

    Args:
        GET:
            album_name: string 

        PSOT(*for ajax only):
            files: [name: 'Filedata']
            album_name: string 

    Returns:
        GET:
            album data

        POST:
            status: {success: true/false, url: url}
    """
    if request.method == 'POST':
        re_helper = ReHelper()
        data = request.files['Filedata']
        album_name = re_helper.r_slash(request.form['album_name'])
        filename = secure_filename(data.filename)
        helper = UpYunHelper()
        url = helper.up_to_upyun('gallery', data, filename)

        if url:
            photo = Photo(title=filename)
            photo.url = url
            photo.album_name = album_name
            photo.save()

            return json.dumps({'success': 'true', 'url': url})
        else:
            return json.dumps({'success': 'false'})
    else:
        if album_name == 'undefined':
            photos = Photo.objects(album_name=u'未分类')
        else:
            photos = Photo.objects(album_name=album_name)

        return render_template('admin/gallery/detail.html', photos=photos)


@admin.route('/photo/del/<album_name>/<photo_id>')
@login_required
def photo_del(album_name, photo_id):
    """Admin Photo Delete Action

    Used for delete Photo.

    Methods:
        GET

    Args:
        album_name: string
        photo_id: photo_id ObjectID

    Returns:
        none
    """
    Photo.objects(pk=photo_id).delete()

    return redirect(url_for('admin.album_detail', album_name=album_name))


@admin.route('/cmspage/edit/<page_url>', methods=['GET', 'POST'])
@login_required
def cmspage_edit(page_url):
    """CMS page edit or create.

    Action for CMS Page.
    Receives title, content(html), tags and cagetory
    Save title, content(html), pure content(further use), page_url
    also auto save author as current_user.

    Methods:
        GET and POST

    Args:
        POST:
            title: page title
            html: content html
            url: page url
        GET:
            page_url: string

    Returns:
        POST:
            none (for create or save page only)
        GET:
            page object or none

    Save:
        title: string
        html: string
        content: string without html tags
        url: string page_url
        summary: first 80 characters in content with 3 dots in the end
        author: current_user_object
    """
    if request.method == 'POST':
        re_helper = ReHelper()

        title = re_helper.r_slash(request.form["title"])
        html = request.form["content"]
        url = request.form["url"]

        parser = MyHTMLParser()
        parser.feed(html)
        content = parser.html # the pure content without html tags

        author = UserModel.objects.first()

        created = StaticPage.objects(url=url)

        if created:
            page = created[0]
        else:
            page = StaticPage(title=title, url=re_helper.r_slash(url))

        page.content = content
        page.summary = content[0:80] + '...'
        page.html = html
        page.author = author
        page.save()

        return redirect(url_for('admin.cmspage_list'))

    else:
        page = StaticPage.objects(url=page_url).first()

        return render_template('admin/page/edit.html', page=page)


@admin.route('/cmspage/list', methods=['GET'])
@login_required
def cmspage_list():
    """Admin CmsPage lit page.

    show all staticPages.

    Methods:
        GET

    Args:
        none

    Returns:
        StaticPage object
    """
    pages = StaticPage.objects.order_by('-publish_time')
    return render_template('admin/page/list.html', pages=pages)


@admin.route('/cmspage/del/<page_url>', methods=['GET'])
@login_required
def cmspage_del(page_url):
    """Admin StaticPage Delete Action

    Used for delete Category.

    Methods:
        GET

    Args:
        page_url: string

    Returns:
        none
    """
    StaticPage.objects.get_or_404(url=page_url).delete()
    return redirect(url_for("admin.cmspage_list"))
