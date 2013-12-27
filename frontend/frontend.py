# -*- coding: utf-8 -*-
import json
import datetime
from operator import attrgetter
import PyRSS2Gen
from flask import (Blueprint, render_template, redirect, request, url_for,
                  make_response, abort)
from jinja2 import TemplateNotFound
from model.models import (User, Diary, Category, CommentEm, Comment, Tag,
                          Photo, StaticPage)
from config import *
from tasks.email_tasks import send_email_task

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
        pages: used for top-nav
        profile: user object
        next_page: boolen
    """
    profile = User.objects.first()
    diaries_all = Diary.objects.order_by('-publish_time')
    diaries = diaries_all[:5]
    diary_num = len(diaries_all)
    if diary_num > 5:
        next_page = True
    else:
        next_page = False

    categories = Category.objects.order_by('-publish_time')
    pages = StaticPage.objects.all()

    return render_template('frontend/home.html', diaries=diaries,
                           categories=categories, pages=pages, profile=profile,
                           next_page=next_page)


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
        pages: used for top-nav
        profile: user object
        prev: if has previous diary
        next: if has next diary
    """
    profile = User.objects.first()
    diary = Diary.objects(pk=diary_id).first()
    categories = Category.objects.order_by('-publish_time')
    pages = StaticPage.objects.all()

    diary_first = Diary.objects.order_by('-publish_time').first()
    diary_last = Diary.objects.order_by('publish_time').first()

    if diary_first == diary:
        prev = False
    else:
        prev = True

    if diary_last == diary:
        next = False
    else:
        next = True

    guest_name = request.cookies.get('guest_name')
    guest_email = request.cookies.get('guest_email')

    return render_template('frontend/diary/detail.html', diary=diary,
                           categories=categories, guest_name=guest_name,
                           guest_email=guest_email, pages=pages, profile=profile,
                           prev=prev, next=next)


@frontend.route('/diary/route/<prev_or_next>/<diary_id>')
def diary_prev_or_next(prev_or_next, diary_id):
    """ Diary Next_Or_Prev page function.

    show next or previous diary details.

    Args:
        prev_or_next: string 'next' or 'prev'
        diary_id: ObjectedId

    Return:
        redirect: diary_detail_page
    """
    if prev_or_next == 'next':
        diary = Diary.objects(pk=diary_id).first()
        next_diary = Diary.objects(publish_time__lt=diary.publish_time
                                       ).order_by('-publish_time').first()
    elif prev_or_next == 'prev':
        diary = Diary.objects(pk=diary_id).first()
        next_diary = Diary.objects(publish_time__gt=diary.publish_time
                                   ).first()

    try:
        return redirect(url_for('frontend.diary_detail', diary_id=next_diary.pk,
                                diary_title=next_diary.title))
    except:
        abort (404)


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
        pages: used for top-nav
        page_num: current page_num
        profile: user object
    """
    next_page = False
    diary_num = len(Diary.objects)
    categories = Category.objects.order_by('-publish_time')
    profile = User.objects.first()
    pages = StaticPage.objects.all()

    diaries = Diary.objects.order_by('-publish_time')[(int(page_num) - 1) * 5
                                                      :int(page_num) * 5]

    if diary_num > int(page_num) * 5:
        next_page = True

    return render_template('frontend/diary/list.html', diaries=diaries,
                           categories=categories, next_page=next_page,
                           page_num=page_num, pages=pages, profile=profile)


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
        pages: used for top-nav
        profile: user object
    """
    next_page = False
    diary_num = len(Category.objects(pk=category_id)[0].diaries)
    if diary_num > 5:
        next_page = True

    profile = User.objects.first()
    categories = Category.objects.order_by('-publish_time')
    pages = StaticPage.objects.all()
    diaries = sorted(Category.objects(pk=category_id)[0].diaries,
                     key=attrgetter('publish_time'),
                     reverse=True)[:5]


    return render_template('frontend/category/list.html',
                           category=category_name, diaries=diaries,
                           categories=categories, next_page=next_page,
                           page_num=1, category_id=category_id, pages=pages,
                           profile=profile)


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
        pages: used for top-nav
        profile: user object
    """
    next_page = False
    diary_num = len(Category.objects(pk=category_id)[0].diaries)

    if diary_num > (int(page_num) - 1) * 5 + 5:
        next_page = True

    profile = User.objects.first()
    categories = Category.objects.order_by('-publish_time')
    pages = StaticPage.objects.all()
    diaries = sorted(Category.objects(pk=category_id)[0].diaries,
                     key=attrgetter('publish_time'),
                     reverse=True)[(int(page_num) - 1) * 5 :int(page_num) * 5]

    return render_template('frontend/category/list.html',
                           category=category_name, diaries=diaries,
                           categories=categories, next_page=next_page,
                           page_num=page_num, category_id=category_id,
                           pages=pages, profile=profile)


@frontend.route('/tag/<tag_name>')
def tag_list(tag_name):
    """ TagList Page.

    used for list diaries with the same tag_name with 5 diaries each page.

    Args:
        tag_name: string

    Return:
        categories: used for sidebar list
        pages: used for top-nav
        diaries: sorted diaries_object by publish_time
        page_num: 1
        tag: tag_name used for title
        profile: user object
    """
    tags = Tag.objects.get_or_404(name=tag_name)
    profile = User.objects.first()
    next_page = False
    diary_num = len(tags.diaries)
    if diary_num > 5:
        next_page = True

    categories = Category.objects.order_by('-publish_time')
    pages = StaticPage.objects.all()
    diaries = sorted(Tag.objects(name=tag_name)[0].diaries,
                     key=attrgetter('publish_time'),
                     reverse=True)[:5]

    return render_template('frontend/tag/list.html', diaries=diaries,
                           categories=categories, tag=tag_name,
                           next_page=next_page, page_num=1, pages=pages,
                           profile=profile)


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
        pages: used for top-nav
        profile: user object
    """
    next_page = False
    diary_num = len(Tag.objects(name=tag_name)[0].diaries)
    if diary_num > int(page_num) * 5:
        next_page = True

    profile = User.objects.first()
    categories = Category.objects.order_by('-publish_time')
    pages = StaticPage.objects.all()
    diaries = sorted(Tag.objects(name=tag_name)[0].diaries,
                     key=attrgetter('publish_time'),
                     reverse=True)[(int(page_num) - 1) * 5 :int(page_num) * 5]

    return render_template('frontend/tag/list.html', diaries=diaries,
                           categories=categories, tag=tag_name,
                           next_page=next_page, page_num=page_num, pages=pages,
                           profile=profile)


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
            send_email_task(Config.EMAIL,
                            Config.MAIN_TITLE + u'收到了新的评论, 请查收',
                            content, did, name, diary_title)

            response = make_response(json.dumps({'success': 'true'}))
            response.set_cookie('guest_name', name)
            response.set_cookie('guest_email', email)
            return response
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
    articles = Diary.objects.order_by('-publish_time')[:12]
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
    ).to_xml('utf-8')
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
        pages: used for top-nav
    """
    photos = Photo.objects.order_by('-publish_time')
    categories = Category.objects.order_by('-publish_time')
    profile = User.objects.first()
    pages = StaticPage.objects.all()

    return render_template('frontend/gallery/index.html', photos=photos,
                           categories=categories, profile=profile, pages=pages)


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
        pages: used for top-nav
        profile: user object
    """
    profile = User.objects.first()
    categories = Category.objects.order_by('-publish_time')
    pages = StaticPage.objects.all()
    page = StaticPage.objects.get_or_404(url=page_url)

    return render_template('frontend/page/index.html', page=page,
                           categories=categories, pages=pages, profile=profile)
