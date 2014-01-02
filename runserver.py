# -*- coding: utf-8 -*-
from tornado.options import define, options
from tornado.log import enable_pretty_logging
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.web

from flask import Flask, render_template, send_from_directory
from config import *
from frontend.frontend import frontend
from admin.admin import admin, User
from model.models import db
from model.models import User as UserModel

import logging
from logging.handlers import SMTPHandler
from utils.email_util import EncodingFormatter

from flask.ext.login import LoginManager

from flask_debugtoolbar import DebugToolbarExtension

USED_CONF = 'config.ProductionConfig'

app = Flask(__name__)
app.register_blueprint(frontend)
app.register_blueprint(admin, url_prefix='/admin')


app.config.from_object(USED_CONF)

login_manager = LoginManager()
login_manager.login_view = "admin.login"
login_manager.login_message = u"Please log in to access this page."


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@login_manager.user_loader
def load_user(id):
    user = UserModel.objects.first()
    return User(user.name, user.pk)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('frontend/404.html'), 404


@app.errorhandler(500)
def special_exception_handler(error):
    return render_template('frontend/404.html'), 500

login_manager.init_app(app)

DebugToolbarExtension(app)

db.init_app(app)

mail_handler = SMTPHandler(
    secure=(),
    mailhost=(SmtpConfig.SERVER, SmtpConfig.PORT),
    fromaddr=SmtpConfig.USER,
    toaddrs=Config.EMAIL,
    subject="%s GOT A SERIOUS PROBLEM" % Config.MAIN_TITLE.encode('utf-8'),
    credentials=(SmtpConfig.USER, SmtpConfig.PASSWORD)
)

mail_handler.setLevel(logging.ERROR)
app.logger.addHandler(mail_handler)
mail_handler.setFormatter(EncodingFormatter('%(message)s', encoding='utf-8'))

define("port", default=8888, help="run on the given port", type=int)

if USED_CONF == 'config.ProductionConfig':
    env = False
else:
    env = True


def main():
    tornado.web.Application(debug=env)
    http_server = HTTPServer(WSGIContainer(app))
    enable_pretty_logging()
    options.parse_command_line()
    http_server.listen(options.port)
    IOLoop.instance().start()
    print 'Quit the server with CONTROL-C'

if __name__ == "__main__":
    main()
