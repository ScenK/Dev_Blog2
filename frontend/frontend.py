# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def show():
    try:
        return render_template('frontend/index.html')
    except TemplateNotFound:
        abort(404)
