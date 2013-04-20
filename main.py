# -*- coding: utf-8 -*- 
import flask
from jinja2 import TemplateNotFound
import data
from auth_util import requires_auth
static_page = flask.Blueprint('static_page', __name__)

@static_page.route('/')
@static_page.route('/st_content/<page_name>')
def show(page_name = None):
    try:
		if not page_name:
			return flask.render_template('base.html', content_name = 'content/tdodin.html')
		else:
			return flask.render_template('base.html', content_name = 'content/' + page_name + '.html')
		
    except TemplateNotFound:
		return page_name
        # abort(404)
	
	
load_price_frm = flask.Blueprint('load_price_frm', __name__)
@load_price_frm.route('/load_file', methods=['GET'])
@requires_auth
def show():
	return flask.render_template('frm_load_file.html')

@load_price_frm.route('/load_file', methods=['POST'])
@requires_auth
def load():
	f = flask.request.files['file']
	if f:  
		if f.filename.rsplit('.', 1)[1].upper() == 'XLS':
			update_type = flask.request.form['update_type']
			price_type = flask.session.get('user_group')
			if not price_type:
				price_type = 'RETAIL'
			return flask.Response(data.LoadXLS(f.read(), update_type, price_type), 200)	
			
			return flask.Response(f.filename, 200)
		else:	
			return flask.Response(u'Нужен xls-файл', 200)
			
	else:	
		return flask.Response(u'Надо выбрать файл.', 200)

##########################################################		

category_page = flask.Blueprint('category_page', __name__)
@category_page.route('/category/<cat_code>', methods=['GET'])
def show(cat_code):
	return flask.render_template('category.html',
				products = data.GetProducts(cat_code),
				categories = data.GetCategories(cat_code),				
				Current_Path = data.GetCurrentPath(cat_code),
				Current_Node = data.GetCurrentNode(cat_code)
				)
		
