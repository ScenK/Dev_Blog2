# -*- coding: utf-8 -*-
import json
from werkzeug import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask.ext.login import (current_user, login_required,
                            login_user, logout_user, UserMixin)
from jinja2 import TemplateNotFound

from Model.models import (Diary, Category, Comment, Tag, Gallery, StaticPage,
                          CommentEm, PhotoEm)
from Model.models import User as UserModel
from utils.email_util import send_reply_mail
from utils.helper.html_helper import MyHTMLParser
from utils.helper.upyun_helper import UpYunHelper

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


@admin.route('/diary/add', methods=['GET', 'POST'])
@login_required
def diary_add():
    """ Add a new diary from admin

    Receives title, content(html), tags and cagetory
    Save title, content(html), pure content(further use), tags and cagetory
    also auto save author as current_user.

    This method will auto save new Category or Tag if not exist otherwise save
    in existed none with push only diary_object

    Args:
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
    categories = Category.objects.all()
    if request.method == 'POST' and 'title' and 'content' in request.form:
        title = request.form["title"]
        html = request.form["content"]
        category = request.form["category"]
        tags = request.form["tags"]

        parser = MyHTMLParser()
        parser.feed(html)
        content = parser.html # the pure content without html tags

        splited_tags = tags.split(',')

        author = UserModel.objects.first()

        post = Diary(title=title)
        post.content = content
        post.summary = content[0:80] + '...'
        post.html = html
        post.author = author
        post.tags = splited_tags
        post.save()

        a, cat = Category.objects.get_or_create(name=category,
                                                defaults={'diaries': [post]})
        if not cat:
            Category.objects(name=category).update_one(push__diaries=post)

        for i in splited_tags:
            b, tag = Tag.objects.get_or_create(name=i,
                                               defaults={'diaries': [post]})
            if not tag:
                Tag.objects(name=i).update_one(push__diaries=post)

        return redirect(url_for("admin.diary_list"))

    return render_template('admin/diary/add.html', categories=categories)


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
    diary = Diary.objects.get_or_404(pk=diary_id)
    categories = Category.objects.all()

    if request.method == 'POST' and 'title' and 'content' in request.form:
        title = request.form["title"]
        html = request.form["content"]
        category = request.form["category"]
        tags = request.form["tags"]

        ''' save simple data for further use'''
        parser = MyHTMLParser()
        parser.feed(html)
        content = parser.html # the pure content without html tags

        splited_tags = tags.split(',')

        diary.content = content
        diary.summary = content[0:80] + '...'
        diary.html = html
        diary.tags = splited_tags
        diary.save()

        a, cat = Category.objects.get_or_create(name=category,
                                                defaults={'diaries': [diary]})
        if not cat:
            Category.objects(name=category).update_one(push__diaries=diary)

        for i in splited_tags:
            b, tag = Tag.objects.get_or_create(name=i,
                                               defaults={'diaries': [diary]})
            if not tag:
                Tag.objects(name=i).update_one(push__diaries=diary)

        return redirect(url_for("admin.diary_list"))

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

    Used for delete Diary.

    Methods:
        GET

    Args:
        diary_id: diary ObjectID

    Returns:
        none
    """
    Diary.objects.get_or_404(pk=diary_id).delete()
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
                    author = current_user.name,
                    content = content,
                )
        post.update_one(push__comments=commentEm)

        ''' Save in Comment Model for admin manage'''
        comment = Comment(content=content)
        comment.diary = post[0]
        comment.author = current_user.name
        comment.save(validate=False)

        try:
            send_reply_mail(email, u'您评论的文章《' + title + u'》收到了来自\
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
    user = UserModel.objects().first()
    if request.method == 'POST':
        username = request.form['username']
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']
        signature = request.form['signature']
        email = request.form['email']

        if pass1 and pass2 and pass1 == pass2:
            user.password = generate_password_hash(password=pass1)

        if username:
            user.name = username

        if signature:
            user.signature = signature

        if email:
            user.email = email

        user.save()

        if pass1 or username:
            logout_user()
            flash(u"请重新登陆")
            return redirect(url_for("admin.index"))

        return redirect(url_for("admin.account_settings"))
    else:
        return render_template('admin/account/settings.html', user=user)


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



@admin.route('/gallery/list', methods=['GET', 'POST'])
@login_required
def gallery_list():
    """Admin Gallery list Page.

    for look up all albums and create a new album.

    Methods:
        GET and POST

    Args:
        GET:
            none

        POST:
            title: string of album title

    Returns:
        GET:
            all albums

        POST:
            status: {status: success}
    """
    if request.method == 'POST':
        title = request.form['title']

        album = Gallery(title=title)
        album.save()

        return json.dumps({'success': 'true'})
    else:
        albums = Gallery.objects.order_by('-publish_time')

        return render_template('admin/gallery/list.html', albums=albums)



@admin.route('/album/detail/<album_id>', methods=['GET', 'POST'])
@login_required
def album_detail(album_id):
    """Album Detail Admin Page.

    Used for upload new photos to UpYun and set deail about album.

    Methods:
        GET and POST

    Args:
        GET:
            album ObjectID

        PSOT(*for ajax only):
            files: [name: 'Filedata']
            album_id: album ObjectID

    Returns:
        GET:
            album data

        POST:
            status: {success: true/false, url: url}
    """
    if request.method == 'POST':
        data = request.files['Filedata']
        album_id = request.form['album_id']
        filename = secure_filename(data.filename)
        helper = UpYunHelper()
        url = helper.up_to_upyun('gallery', data, filename)
        if url:
          photo = PhotoEm(
                    path = url,
                    title = filename
                  )
          Gallery.objects(pk=album_id).update_one(push__content=photo)
          return json.dumps({'success': 'true', 'url': url})
        else:
          return json.dumps({'success': 'false'})
    else:
        album = Gallery.objects(pk=album_id)[0]

        return render_template('admin/gallery/detail.html', album=album)
    

@admin.route('/album/del/<album_id>')
@login_required
def album_del(album_id):
    """Admin Album Delete Action

    Used for delete Album.

    Methods:
        GET

    Args:
        album_id: album ObjectID

    Returns:
        none
    """
    Gallery.objects.get_or_404(pk=album_id).delete()
    return redirect(url_for("admin.gallery_list"))


@admin.route('/photo/del/<album_id>/<photo_title>')
@login_required
def photo_del(album_id, photo_title):
    """Admin Photo Delete Action

    Used for delete Photo.

    Methods:
        GET

    Args:
        album_id: album_id ObjectID
        photo_title: string title of photo 

    Returns:
        none
    """
    Gallery.objects(pk=album_id).update_one(pull__content={'title': photo_title})

    return redirect(url_for('admin.album_detail', album_id=album_id))

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
        title = request.form["title"]
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
            page = StaticPage(title=title, url=url)

        page.content = content
        page.summary = content[0:80] + '...'
        page.html = html
        page.author = author
        page.save()

        return redirect(url_for('admin.index'))

    else:
        page = StaticPage.objects(url=page_url).first()

        return render_template('admin/page/edit.html', page=page)
