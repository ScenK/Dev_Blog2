# -*- coding: utf-8 -*-

import os
import re
from fabric.api import task, execute, local
import datetime
from werkzeug.security import generate_password_hash
from mongoengine import connect
from blog.config import Config
from blog.model.models import User

connect(Config.MONGODB_SETTINGS.get('DB'))


@task
def deploy():
    execute(lessc)
    execute(compress)
    execute(backup_database)


@task
def start():
    local("python blog/runserver.py --port=8000")


@task
def test():
    local("python blog/blog_tests.py")


@task
def build():
    user = User(name='admin')
    user.password = generate_password_hash(password='admin')
    user.save()
    print "Default Admin add Success!"
    execute(deploy)


@task
def compress():
    execute(compress_css)
    execute(compress_all_js)


@task
def compress_all_js():
    compress_js('blog/admin/static', 'backend')
    compress_js('blog/static', 'frontend')
    compress_js('blog/static', '404')


@task
def compress_js(folder, debug_files):
    js_files = []

    target = open(folder + '/js/' + debug_files + '.js', "r")
    p = re.compile("document.*src=\'/(.*?)\'.*")
    for line in target:
        m = p.match(line)
        if m:
            js_files.append(m.group(1))
    target.close()

    local("rm -f %s/js/%s.min*.js" % (folder, debug_files))

    compressed_file = "%s/js/%s.min.js" % (folder, debug_files)
    for f in js_files:
        local(
            'java -jar blog/yuicompressor.jar --charset utf-8 --type js %s >> %s' %
            ('blog/' + f, compressed_file))


@task
def compress_css():
    css_files = ['frontend', '404']

    local("rm -f blog/static/css/*.min*.css")

    for f in css_files:
        local(
            'java -jar blog/yuicompressor.jar --charset utf-8 --type css %s >> %s' %
            ('blog/static/css/' + f + '.css', 'blog/static/css/' + f + '.min.css'))

    local("rm -f blog/admin/static/css/admn.min.css")

    local(
        'java -jar blog/yuicompressor.jar --charset utf-8 --type css %s >> %s' %
        ('blog/admin/static/css/admin.css', 'blog/admin/static/css/admin.min.css'))


@task
def lessc():
    local("lessc blog/static/less/frontend.less > blog/static/css/frontend.css")
    local("lessc blog/static/less/404.less > blog/static/css/404.css")


@task
def update():
    local("git pull")
    execute(deploy)


@task
def backup_database():
    local("sudo rm -rf ~/mongobak")
    local("mongodump -d %s -o ~/mongobak" % Config.MONGODB_SETTINGS.get('DB'))
    local("tar -czvPf ~/%s_%s.tar.gz ~/mongobak/*" %
          (Config.MONGODB_SETTINGS.get('DB'),
           datetime.datetime.now().strftime("%Y%m%d%H%M%S")))


@task
def count_line():
    exts = ['.py', '.js', '.html', '.css']
    for i in exts:
        count = 0
        fcount = 0
        for root, dirs, files in os.walk(os.getcwd() + '/blog'):
            for f in files:
                # Check the sub directorys
                fname = (root + '/' + f)
                try:
                    ext = f[f.rindex('.'):]
                except:
                    pass

                if '.git' not in fname and i == ext:
                    fcount += 1
                    c = read_line_count(fname)
                    count += c

        print '%s ==> has %d files and %d lines' % (i, fcount, count)


def read_line_count(fname):
    count = 0
    with open(fname, 'r') as f:
        for file_line in f:
            count += 1
        return count
