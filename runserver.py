# -*- coding: utf-8 -*-
from tornado.options import define, options
from tornado.log import enable_pretty_logging
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from flask import Flask, render_template, send_from_directory
from config import *
from frontend.frontend import frontend
from admin.admin import admin, User
from Model.models import db
from Model.models import User as UserModel

from flask.ext.login import LoginManager

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.register_blueprint(frontend)
app.register_blueprint(admin, url_prefix='/admin')


app.config.from_object('config.ProductionConfig')

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

@app.errorhandler(500)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('frontend/404.html'), 404

login_manager.init_app(app)

DebugToolbarExtension(app)

db.init_app(app)

define("port", default=8888, help="run on the given port", type=int)

def main():
    http_server = HTTPServer(WSGIContainer(app))
    enable_pretty_logging()
    options.parse_command_line()
    http_server.listen(options.port)
    IOLoop.instance().start()
    print 'Quit the server with CONTROL-C'

if __name__ == "__main__":
    main()
