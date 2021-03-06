# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, redirect, request, url_for,
                   abort, Response)

from config import Config

from dispatcher import (UserDispatcher, DiaryDispatcher, CategoryDispatcher,
                        TagDispatcher, PageDispatcher, OtherDispatcher,
                        CommentDispatcher)

frontend = Blueprint('frontend', __name__, template_folder='templates',
                     static_folder='static')

root = Config.THEME

templates = dict(
    home="frontend/themes/%s/home.html" % root,
    diary_detail="frontend/themes/%s/diary/detail.html" % root,
    diary_list="frontend/themes/%s/diary/list.html" % root,
    cat_list="frontend/themes/%s/category/list.html" % root,
    tag_list="frontend/themes/%s/tag/list.html" % root,
    page="frontend/themes/%s/page/index.html" % root,
    not_found="frontend/themes/%s/404.html" % root
)

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
    page_size = 5

    profile = UserDispatcher().get_profile()
    categories = CategoryDispatcher().get_all_categories()
    pages = PageDispatcher().get_all_pages()
    prev, next, diaries = DiaryDispatcher().get_diary_list(0, page_size)

    return render_template(templates['home'],
                           diaries=diaries, categories=categories,
                           pages=pages, profile=profile, next_page=next)


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
    profile = UserDispatcher().get_profile()

    prev, next, diary = DiaryDispatcher().get_diary_width_navi(diary_id=diary_id)

    categories = CategoryDispatcher().get_all_categories()

    pages = PageDispatcher().get_all_pages()

    guest_name = request.cookies.get('guest_name')
    guest_email = request.cookies.get('guest_email')

    return render_template(templates['diary_detail'],
                           diary=diary, categories=categories,
                           guest_name=guest_name, guest_email=guest_email,
                           pages=pages, profile=profile, prev=prev, next=next)


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

    next_diary = DiaryDispatcher().get_next_or_prev_diary(prev_or_next,
                                                          diary_id)

    try:
        return redirect(
            url_for('frontend.diary_detail', diary_id=next_diary.pk,
                    diary_title=next_diary.title))
    except Exception as e:
        print(str(e))
        abort(404)


@frontend.route('/diary/list/<int:page_num>')
@frontend.route('/category/<cat_name>')
@frontend.route('/category/<cat_name>/page/<int:page_num>')
@frontend.route('/tag/<tag_name>')
@frontend.route('/tag/<tag_name>/page/<int:page_num>')
def diary_list(page_num=None, cat_id=None, cat_name=None, tag_name=None):
    """Diary list page.

    listed 5 diaries each page.Adjusted for diary, category and tag pagging.

    Args:
        page_num: numberic and int
        cate_name: string, can be none
        tag_name: string, can be none

    Return:
        diaries: listed 5 diaries objects
        next: bool True or False
        prev: bool True or False
        categories: used for sidebar
        pages: used for top-nav
        page_num: current page_num
        profile: user object
    """
    page_size = 5

    profile = UserDispatcher().get_profile()
    categories = CategoryDispatcher().get_all_categories()
    pages = PageDispatcher().get_all_pages()

    if not page_num:
        page_num = 1

    start = (int(page_num) - 1) * page_size
    end = int(page_num) * page_size

    if tag_name:
        prev, next, diaries = TagDispatcher().get_diary_list_with_navi(
            tag_name, start, end)
        tpl = 'tag_list'
    elif cat_name:
        prev, next, diaries = CategoryDispatcher().get_diary_list_with_navi(
            cat_name, start, end)
        tpl = 'cat_list'
    else:
        prev, next, diaries = DiaryDispatcher().get_diary_list(start, end)
        tpl = 'diary_list'

    return render_template(templates[tpl], diaries=diaries,
                           categories=categories, next_page=next,
                           prev_page=prev, page_num=page_num, pages=pages,
                           profile=profile, cat_name=cat_name, tag_name=tag_name)


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
        author = request.form['username']
        diary_id = request.form['did']
        email = request.form['email']
        content = request.form['comment']

        return CommentDispatcher().add_comment(author, diary_id, email, content)


@frontend.route('/feed')
def rss():
    """ RSS2 Support.

        support xml for RSSItem with 12 diaries.

    Args:
        none
    Return:
        none
    """
    content = OtherDispatcher().get_rss(12)

    return Response(content, mimetype='text/xml')


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
    profile = UserDispatcher().get_profile()
    categories = CategoryDispatcher().get_all_categories('-publish_time')
    pages = PageDispatcher().get_all_pages('-publish_time')
    page = PageDispatcher().get_page(page_url=page_url)

    return render_template(templates['page'], page=page,
                           categories=categories, pages=pages, profile=profile)
