# -*- coding: utf-8 -*- 
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import data

static_page = Blueprint('static_page', __name__)

@static_page.route('/')
@static_page.route('/st_content/<page_name>')
def show(page_name = None):
    try:
		if not page_name:
			return render_template('base.html', content_name = 'content/tdodin.html')
		else:
			return render_template('base.html', content_name = 'content/' + page_name + '.html')
		
    except TemplateNotFound:
		return page_name
        # abort(404)

		
cat_page = Blueprint('cat_page', __name__)

@cat_page.route('/test/<page>')
def show(page):
	return render_template('base.html', content_name = 'content/tree.html', items=data.GetTree())
	

	
    # if request.method == 'POST':
        # if request.form['username'] != app.config['USERNAME']:
            # error = 'Invalid username'
        # elif request.form['password'] != app.config['PASSWORD']:
            # error = 'Invalid password'
        # else:
            # session['logged_in'] = True
            # flash('You were logged in')
            # return redirect(url_for('/'))
    # return render_template('login.html', error=error)	