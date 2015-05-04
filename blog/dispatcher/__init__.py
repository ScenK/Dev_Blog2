# -*- coding: utf-8 -*-

import json
import datetime
import PyRSS2Gen
from werkzeug.security import generate_password_hash
from mongoengine.errors import NotUniqueError, ValidationError
from flask import make_response
from tasks.email_tasks import send_email_task

from config import Config
from model.models import (User, Diary, Category, Page, Tag, Comment,
                          CommentEm, StaticPage)
from utils.helper import SiteHelpers


class UserDispatcher(object):
    """User dispatcher.
    Return author profile
    """
    def get_profile(self):
        """Return User object."""
        return User.objects.first()

    def generate_user(self, username, password):
        """Generate User"""
        user = User(name=username)
        user.password = generate_password_hash(password=password)
        return user.save()

    def delete_user(self):
        """Delete User"""
        return User.objects().first().delete()

    def get_by_name(self, username):
        """Get user by username

        Args:
            username: string

        Return:
            user: user object
        """
        return User.objects(name=username).first()


class CommentDispatcher(object):
    """Comment dispatcher.
    Retuen comments functons helper.
    """
    def add_comment(self, author, diary_id, email, content):
        diary = Diary.objects(pk=diary_id)
        diary_title = diary.first().title
        comment_em = CommentEm(
            author=author,
            content=content,
            email=email
        )
        diary.update_one(push__comments=comment_em)

        comment = Comment(content=content)
        comment.diary = diary.first()
        comment.email = email
        comment.author = author
        comment.save(validate=False)

        try:
            send_email_task(Config.EMAIL,
                            Config.MAIN_TITLE + u'收到了新的评论, 请查收',
                            content, diary_id, author, diary_title)

            response = make_response(json.dumps({'success': 'true'}))
            response.set_cookie('guest_name', author)
            response.set_cookie('guest_email', email)

            return response
        except Exception as e:
            return str(e)

    def reply_comment(self, author, diary_id, email, content):
        diary = Diary.objects(pk=diary_id)
        diary_title = diary.first().title
        comment_em = CommentEm(
            author=u'博主回复',
            content=content,
        )
        diary.update_one(push__comments=comment_em)

        ''' Save in Comment model for admin manage'''
        comment = Comment(content=content)
        comment.diary = diary.first()
        comment.author = UserDispatcher().get_profile().name
        comment.save(validate=False)

        try:
            send_email_task(email, u'您评论的文章《' + diary_title + u'》收到了来自\
                            博主的回复, 请查收', content, diary_id, author,
                            diary_title)

            return json.dumps({'success': 'true'})
        except Exception as e:
            return json.dumps({'success': 'false', 'reason': str(e)})

    def get_all_comments(self, order='-publish_time'):
        """Return Total diaries objects."""
        return Comment.objects.order_by(order)

    def del_comment_by_id(self, comment_id):
        """Comment delete by id.
        Also remove comment from diary detail

        Args:
            comment_id: Object_id.

        Return:
            None
        """
        comment = Comment.objects.get_or_404(pk=comment_id)

        diary = Diary.objects(pk=comment.diary.pk)

        diary.update_one(pull__comments={'content': comment.content})

        return comment.delete()

    def get_comment_list(self, start=0, end=20, order='-publish_time'):
        """Comment list.
        default query 20 comments and return if there should be next or prev
        page.

        Args:
            start: num defalut 0
            end: num defalut 20
            order: str defalut '-publish_time'

        Return:
            next: boolean
            prev: boolean
            comments: diaries list
        """
        size = end - start
        prev = next = False
        comments = Comment.objects.order_by(order)[start:end + 1]
        if len(comments) - size > 0:
            next = True
        if start != 0:
            prev = True

        return prev, next, comments[start:end]


class DiaryDispatcher(object):
    """ Diary dispatcher.
    Return diary collection objects.
    """

    def get_all_diaries(self, order='-publish_time'):
        """Return Total diaries objects."""
        return Diary.objects.order_by(order)

    def get_by_id(self, diary_id):
        """Diary detail.
        Only return diary detail by diary_id.

        Args:
            diary_id: objectID

        Return:
            diary: diary object
        """
        try:
            diary = Diary.objects(pk=diary_id).first()
        except ValidationError:
            diary = None

        return diary

    def get_diary_width_navi(self, diary_id):
        """Diary Detail Width page navi boolean.
        get diary detail and if there should be prev or next page.

        Args:
            diary_id: objectID

        Return:
            diary: diary object
            prev: boolean, can be used as 'prev' logic
            next: boolean, can be used as 'next' logic
        """
        prev = next = True

        diary = self.get_by_id(diary_id)

        if diary == self.get_first_diary():
            next = False
        if diary == self.get_last_diary():
            prev = False

        return prev, next, diary

    def get_first_diary(self):
        """Return First Diary object."""
        return Diary.objects.order_by('-publish_time').first()

    def get_last_diary(self):
        """Return Last Diary object."""
        return Diary.objects.order_by('publish_time').first()

    def get_prev_diary(self, pub_time):
        """Return Previous Diary object."""
        return Diary.objects(publish_time__lt=pub_time
                             ).order_by('-publish_time').first()

    def get_next_diary(self, pub_time):
        """Return Next Diary object."""
        return Diary.objects(publish_time__gt=pub_time
                             ).order_by('-publish_time').first()

    def get_next_or_prev_diary(self, prev_or_next, diary_id):
        """Diary route prev or next function.
        Use publish_time to determin what`s the routed diary.

        Args:
            prev_or_next: string 'prev' or 'next'
            diary_id: objectID

        Return:
            next_diary: routed diary object
        """
        diary = self.get_by_id(diary_id)

        if prev_or_next == 'prev':
            next_diary = self.get_prev_diary(diary.publish_time)
        else:
            next_diary = self.get_next_diary(diary.publish_time)

        return next_diary

    def get_diary_count(self):
        """Return Diaries total number."""
        return Diary.objects.count()

    def get_diary_list(self, start=0, end=10, order='-publish_time'):
        """Diary list.
        default query 10 diaries and return if there should be next or prev
        page.

        Args:
            start: num defalut 0
            end: num defalut 10
            order: str defalut '-publish_time'

        Return:
            next: boolean
            prev: boolean
            diaries: diaries list
        """
        size = end - start
        prev = next = False
        diaries = Diary.objects.order_by(order)[start:end + 1]
        if len(diaries) - size > 0:
            next = True
        if start != 0:
            prev = True

        return prev, next, diaries[start:end]

    def edit_diary(self, diary_id, title, html, category, tags):
        """ Edit diary from admin

        receives title, content(html), tags and cagetory
        save title, content(html), pure content(further use), tags and cagetory
        also auto save author as current_user.

        this method will auto save new Category or Tag if not exist otherwise
        save in existed none with push only diary_object

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
        title = SiteHelpers().secure_filename(title)
        category = SiteHelpers().secure_filename(category)
        content = SiteHelpers().strip_html_tags(html)
        splited_tags = tags.split(',')

        author = UserDispatcher().get_profile()

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

        return

    def get_or_create_diary(self, diary_id):
        try:
            diary = Diary.objects(pk=diary_id).first()
        except:
            diary = None
        categories = Category.objects.all()

        return diary, categories

    def del_diary_by_id(self, diary_id):
        """Diary delete.
        Also delete diary link from category collection

        Args:
            diary_id: objectID

        Return:
            None
        """
        diary = Diary.objects(pk=diary_id)
        Category.objects(name=diary[0].category).update_one(
            pull__diaries=diary[0])
        return diary.delete()


class CategoryDispatcher(object):
    """Category dispatcher.
    Return category objects
    """
    def get_all_categories(self, order='-publish_time'):
        """Return Total Categories objects."""
        return Category.objects.order_by(order)

    def get_diary_list_with_navi(self, cat_name, start=0, end=10,
                                 order='-publish_time'):
        """Category Diary list.
        default query 10 diaries and return if there should be next or prev
        page.

        Args:
            cat_name: string
            start: num defalut 0
            end: num defalut 10
            order: str defalut '-publish_time'

        Return:
            next: boolean
            prev: boolean
            diaries: diaries list
        """

        size = end - start
        prev = next = False
        diaries = Diary.objects(category=cat_name).order_by(order)[start:
                                                                   end + 1]
        if len(diaries) - size > 0:
            next = True
        if start != 0:
            prev = True

        return prev, next, diaries[start:end]

    def get_category_count(self):
        """Return Categories total number."""
        return Category.objects.count()

    def add_new_category(self, cat_name):
        """Category add new.
        Will check if the cat_name is unique, otherwise will return an error.

        Args:
            cat_name: string category name.

        Return:
            None
        """
        cat_name = SiteHelpers().secure_filename(cat_name)

        try:
            category = Category(name=cat_name)
            return category.save()
        except NotUniqueError:
            return 'category name not unique'

    def get_category_detail(self, cat_id):
        """Category detail.
        will return category detail by category id.

        Args:
            cat_name: string category name.

        Return:
            category: category object
        """
        return Category.objects(pk=cat_id).first()

    def del_category_by_name(self, cat_name):
        """Category delete by name.
        Will check if the cat_name is unique, otherwise will return an error.

        Args:
            cat_name: string category name.

        Return:
            None
        """
        return Category.objects.get_or_404(name=cat_name).delete()


class TagDispatcher(object):
    """Tag dispatcher.
    Return tag objects
    """
    def get_all_tags(self, order='-publish_time'):
        """Return Total Tags objects."""
        return Category.objects.order_by(order)

    def get_diary_list_with_navi(self, tag_name, start=0, end=10,
                                 order='-publish_time'):
        """Tag Diary list.
        default query 10 diaries and return if there should be next or prev
        page.

        Args:
            tag_name: string
            start: num defalut 0
            end: num defalut 10
            order: str defalut '-publish_time'

        Return:
            next: boolean
            prev: boolean
            diaries: diaries list
        """

        size = end - start
        prev = next = False
        diaries = Diary.objects(tags=tag_name).order_by(order)[start: end + 1]
        if len(diaries) - size > 0:
            next = True
        if start != 0:
            prev = True

        return prev, next, diaries[start:end]

    def get_tag_count(self):
        """Return Tags total number."""
        return Tag.objects.count()

    def add_new_tag(self, tag_name):
        """Tag add new.
        Will check if the cat_name is unique, otherwise will return an error.

        Args:
            tag_name: string category name.

        Return:
            None
        """
        tag_name = SiteHelpers().secure_filename(tag_name)

        try:
            category = Tag(name=tag_name)
            return category.save()
        except NotUniqueError:
            return 'tag name not unique'

    def get_tag_detail(self, tag_name):
        """Tag detail.
        will return tag detail by tag name.

        Args:
            tag_name: string tag name.

        Return:
            tag: tag object
        """
        return Tag.objects(name=tag_name).first()


class PageDispatcher(object):
    """Page dispatcher.
    Return page objects
    """
    def get_all_pages(self, order='-publish_time'):
        return Page.objects.order_by(order)

    def get_page(self, page_url):
        return Page.objects(url=page_url).first()

    def get_static_page(self, page_url):
        return StaticPage.objects(url=page_url).first()

    def get_all_static_pages(self, order='-publish_time'):
        return StaticPage.objects.order_by(order)

    def del_cmspage_by_url(self, page_url):
        return StaticPage.objects.get_or_404(url=page_url).delete()

    def edit_or_create_page(self, title, html, url):
        """CMS page edit or create.

        Action for CMS Page.
        Receives title, content(html), tags and cagetory
        Save title, content(html), pure content(further use), page_url
        also auto save author as current_user.

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
        title = SiteHelpers().secure_filename(title)
        content = SiteHelpers().strip_html_tags(html)
        author = UserDispatcher().get_profile()

        created = StaticPage.objects(url=url)

        if created:
            page = created.first()
            page.title = title
        else:
            page = StaticPage(title=title,
                              url=SiteHelpers().secure_filename(url))

        page.content = content
        page.summary = content[0:80] + '...'
        page.html = html
        page.author = author
        return page.save()


class OtherDispatcher(object):

    def up_img_to_upyun(self, collection, data, filename):
        """Up image to upyun collecton.
        Will get back upyun link.

        Args:
            collection: string, collection name
            data: image data
            filename: filename

        Return:
            success: boolean, True/False
            url: url_link
        """
        filename = SiteHelpers().secure_filename(filename)
        success, url = SiteHelpers().up_to_upyun(collection, data, filename)

        return success, url

    def get_rss(self, size):
        """ RSS2 Support.

            support xml for RSSItem with sized diaries.

        Args:
            none
        Return:
            rss: xml
        """
        articles = Diary.objects.order_by('-publish_time')[:size]
        items = []
        for article in articles:
            content = article.html

            url = Config.SITE_URL + '/diary/' + str(article.pk) + '/' + \
                article.title
            items.append(PyRSS2Gen.RSSItem(
                title=article.title,
                link=url,
                description=content,
                guid=PyRSS2Gen.Guid(url),
                pubDate=article.publish_time,
            ))
        rss = PyRSS2Gen.RSS2(
            title=Config.MAIN_TITLE,
            link=Config.SITE_URL,
            description=Config.DESCRIPTION,
            lastBuildDate=datetime.datetime.now(),
            items=items
        ).to_xml('utf-8')
        return rss
