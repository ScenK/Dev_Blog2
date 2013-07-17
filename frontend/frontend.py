# -*- coding: utf-8 -*-
import datetime
import PyRSS2Gen
from flask import Blueprint, render_template, redirect, request, url_for
from jinja2 import TemplateNotFound
from Model.models import (User, Diary, Category, CommentEm, Comment, Tag,
                          Gallery, StaticPage)
from config import *
from utils.email_util import send_reply_mail

frontend = Blueprint('frontend', __name__, template_folder='templates',
                     static_folder='static')

@frontend.route('/')
def home():
    """ HomePage.

     list newest 5 diaries.

    Args: 
        none

    Return:
        diaries: 5 diaries list
        categories: used for sidebar
    """
    diaries = Diary.objects.order_by('-publish_time')[:5]
    categories = Category.objects.order_by('-publish_time')

    return render_template('frontend/home.html', diaries=diaries,
                           categories=categories)


@frontend.route('/diary/<diary_id>/<diary_title>')
def diary_detail(diary_id, diary_title=None):
    """ Diary Detail Page. 

    show diary details.

    Args:
        diary_id: ObjectedId
        diary_title: string used for SEO Only

    Return:
        diary_detail: diary_object
        categories: used for sidebar
        guest_name: string cookie for guest comment auto complete filed
        guest_email: string cookie for guest comment auto complete filed
    """
    diary = Diary.objects(pk=diary_id)[0]
    categories = Category.objects.order_by('-publish_time')

    guest_name = request.cookies.get('guest_name') 
    guest_email = request.cookies.get('guest_email')
    
    return render_template('frontend/diary/detail.html', diary=diary,
                           categories=categories, guest_name=guest_name,
                           guest_email=guest_email)


@frontend.route('/diary/list/<page_num>')
def diary_list(page_num):
    """Diary list page.

    listed 5 diaries each page.

    Args:
        page_num: numberic and int

    Return:
        diaries: listed 5 diaries objects
        next_page: bool True or False
        categories: used for sidebar
        page_num: current page_num
    """
    next_page = False
    diary_num = len(Diary.objects)
    categories = Category.objects.order_by('-publish_time')

    diaries = Diary.objects.order_by('-publish_time')[(int(page_num) - 1) * 5
                                                      :int(page_num) * 5] 

    if diary_num > int(page_num) * 5:
        next_page = True

    return render_template('frontend/diary/list.html', diaries=diaries, 
                           categories=categories, next_page=next_page,
                           page_num=page_num)


@frontend.route('/category/<category_id>/<category_name>')
def category_list(category_id, category_name=None):
    """Category list page.

    show 5 diaries in this page.

    Args:
        category_id: categoryObjectID
        category_name: only for SEO

    Return:
        next_page: bool True or False
        page_num: 1
        category: category_name used for title
        diaries: listed 5 diaries in each page
        categories: used in sidebar
    """
    next_page = False
    diary_num = len(Category.objects(pk=category_id)[0].diaries)
    if diary_num > 5:
        next_page = True

    categories = Category.objects.order_by('-publish_time')
    diaries = sorted(Category.objects(pk=category_id)[0].diaries, 
            reverse=True)[:5]

    return render_template('frontend/category/list.html',
                           category=category_name, diaries=diaries,
                           categories=categories, next_page=next_page,
                           page_num=1, category_id=category_id)


@frontend.route('/category/<category_id>/<category_name>/page/<page_num>')
def category_paging(category_id, page_num, category_name=None):
    """Category list page.

    show 5 diaries in each page.

    Args:
        category_id: categoryObjectID
        category_name: only for SEO
        page_num: page_num

    Return:
        next_page: bool True or False
        page_num: now page_num
        category: category_name used for title
        diaries: listed 5 diaries in each page
        categories: used in sidebar
    """
    next_page = False
    diary_num = len(Category.objects(pk=category_id)[0].diaries)

    if diary_num > (int(page_num) - 1) * 5 + 5:
        next_page = True

    categories = Category.objects.order_by('-publish_time')
    diaries = sorted(Category.objects(pk=category_id)[0].diaries,
                     reverse=True)[(int(page_num) - 1) * 5
                                   :int(page_num) * 5]

    return render_template('frontend/category/list.html',
                           category=category_name, diaries=diaries,
                           categories=categories, next_page=next_page,
                           page_num=page_num, category_id=category_id)


@frontend.route('/tag/<tag_name>')
def tag_list(tag_name):
    """ TagList Page.

    used for list diaries with the same tag_name with 5 diaries each page.

    Args: 
        tag_name: string

    Return:
        categories: used for sidebar list
        diaries: sorted diaries_object by publish_time
        page_num: 1
        tag: tag_name used for title 
    """
    next_page = False
    diary_num = len(Tag.objects(name=tag_name)[0].diaries)
    if diary_num > 5:
        next_page = True

    categories = Category.objects.order_by('-publish_time')
    diaries = sorted(Tag.objects(name=tag_name)[0].diaries, reverse=True)[:5]

    return render_template('frontend/tag/list.html', diaries=diaries,
                           categories=categories, tag=tag_name,
                           next_page=next_page, page_num=1)

@frontend.route('/tag/<tag_name>/page/<page_num>')
def tag_paging(tag_name, page_num):
    """ TagList Paging.

    used for list diaries with the same tag_name with 5 diaries each page.

    Args: 
        tag_name: string
        page_num: page_num

    Return:
        categories: used for sidebar list
        next_page: bool True or False
        diaries: sorted diaries_object by publish_time with 5 each page
        page_num: now page_num
        tag: tag_name used for title 
    """
    next_page = False
    diary_num = len(Tag.objects(name=tag_name)[0].diaries)
    if diary_num > int(page_num) * 5:
        next_page = True

    categories = Category.objects.order_by('-publish_time')
    diaries = sorted(Tag.objects(name=tag_name)[0].diaries,
                     reverse=True)[(int(page_num) - 1) * 5
                                    :int(page_num) * 5]

    return render_template('frontend/tag/list.html', diaries=diaries,
                           categories=categories, tag=tag_name,
                           next_page=next_page, page_num=page_num)


@frontend.route('/comment/add', methods=['POST'])
def comment_add():
    """ Comment Add AJAX Post Action.

    designed for ajax post and send reply email for admin

    Args:
        username: guest_name
        did: diary ObjectedId
        email: guest_email
        content: comment content

    Return:
        email_status: success
    """
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

        comment = Comment(content=content)
        comment.diary = post[0]
        comment.email = email
        comment.author = name
        comment.save(validate=False)

        try:
            send_reply_mail(Config.EMAIL, 
                            Config.MAIN_TITLE + u'收到了新的评论, 请查收',
                            content, did, name, diary_title)
            return 'success'
        except Exception as e:
            return str(e)


@frontend.route('/feed')
def rss():
    """ RSS2 Support.
    
        support xml for RSSItem with 12 diaries.

    Args:
        none
    Return:
        diaries_object: list
        site_settings: title, link, description
    """
    articles = Diary.objects[:12]
    items = []
    for article in articles:
        content = article.html

        url = Config.SITE_URL + '/diary/detail/' + str(article.pk) + '/' + \
              article.title
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


@frontend.route('/gallery')
def gallery():
    """GalleryPage.
     list all photo.

    Args: 
        none

    Return:
        albums : all photos
        categories: used for sidebar
        profile: user object
    """
    albums = Gallery.objects.order_by('-publish_time')
    categories = Category.objects.order_by('-publish_time')
    profile = User.objects.first()

    return render_template('frontend/gallery/index.html', albums=albums,
                           categories=categories, profile=profile)


@frontend.route('/page/<page_url>')
def page(page_url):
    """CMS page.
    show page for page_name.

    Methods:
        POST

    Args:
        page_url: string

    Return:
        categories: used for sidebar
        page object
    """
    categories = Category.objects.order_by('-publish_time')
    page = StaticPage.objects.get_or_404(url=page_url)

    return render_template('frontend/page/index.html', page=page,
                           categories=categories)
