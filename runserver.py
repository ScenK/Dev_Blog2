# -*- coding: utf-8 -*-
from flask import Flask
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

app.config.from_object('config.DevelopmentConfig')

login_manager = LoginManager()
login_manager.login_view = "admin.login"
login_manager.login_message = u"Please log in to access this page."

@login_manager.user_loader
def load_user(id):
    user = UserModel.objects.first()
    return User(user.name, user.pk)  

login_manager.init_app(app)

DebugToolbarExtension(app)

db.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
