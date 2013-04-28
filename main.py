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
			price_type = flask.request.form['PriceType']
			return flask.Response(data.LoadXLS(f.read(), update_type, price_type), 200)	
			
			return flask.Response(f.filename, 200)
		else:	
			return flask.Response(u'Нужен xls-файл', 200)
			
	else:	
		return flask.Response(u'Надо выбрать файл.', 200)

load_images = flask.Blueprint('load_images', __name__)
@load_images.route('/load_images', methods=['GET'])
@requires_auth
def load():
	return flask.Response(data.LoadImages(), 200)	
		
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
		
product_page = flask.Blueprint('product_page', __name__)
@product_page.route('/product/<product_code>', methods=['GET'])
def show(product_code):
	return flask.render_template('product.html',
				Current_Path = data.GetCurrentPath(product_code),
				item = data.GetCurrentProduct(product_code)
				)
				
#########################################################################################

search_page = flask.Blueprint('search_page', __name__)
@search_page.route("/search/")
def show():
	s = flask.request.args.get('q')				
	if not s:
		return flask.render_template('search_result.html',
					result = None,
					page_title = u'Поиск',
					search_str = '',
					message = s
					)
	res = data.search(s)
	if not res:
		msg = u'Ничего не найдено, попробуйте изменить запрос'
	else:
		msg = u'Найдено подходящих товаров: ' + str(len(res))
		
	return flask.render_template('search_result.html',
					results = res,
					page_title = u'Поиск ' + s,
					search_str = s,
					message = msg
					)

#########################################################################################

basket_page = flask.Blueprint('basket_page', __name__)
@basket_page.route("/basket/")
def show():
	return flask.render_template('basket.html',
					items_list = data.GetBasket()
					)
#########################################################################################

order_page = flask.Blueprint('order_page', __name__)
@order_page.route("/order/", methods=['POST'] )
def show():
	s = u''
	codes = []
	for key, value in flask.request.form.items():
		if key[:6] == 'count_' and int(value) > 0:
			codes.append( (key[6:], int(value)) )
			
	order = data.MakeOrder(
		flask.request.form['org_name'],
		flask.request.form['user_name'],
		flask.request.form['user_mail'],
		flask.request.form['user_phone1'],
		flask.request.form['user_phone2'],
		flask.request.form['addr'],
		flask.request.form['remarks'],
		codes
		)
	data.send_mail(order)	
	return flask.Response(order, 200)

	# return flask.render_template('order.html',
					# items_list = data.GetBasket()
					# )
												