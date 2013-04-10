# -*- coding: utf-8 -*- 
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

static_page = Blueprint('static_page', __name__)

@static_page.route('/st_content/<page_name>')
def show(page_name):
    try:
        return render_template('base.html', content_name = 'content/' + page_name + '.html')
    except TemplateNotFound:
		return page_name
        # abort(404)