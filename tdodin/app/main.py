# -*- coding: utf-8 -*- 
import flask
from jinja2 import TemplateNotFound
import data
from auth_util import requires_auth
import json

static_page = flask.Blueprint('static_page', __name__)

@static_page.route('/')
@static_page.route('/st_content/<page_name>')
def show(page_name = None):
    try:
		if not page_name:
			return flask.render_template('main_page.html', content_name = 'content/tdodin.html')
		else:
			return flask.render_template('main_page.html', content_name = 'content/' + page_name + '.html')
		
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
			if update_type == 'COUNT_UPDATE':  #Остатки, у них особый вид файла
				return flask.Response(data.LoadCountsXLS( f.read() ), 200)	
			else:	
				return flask.Response(data.LoadXLS(f.read(), update_type, price_type), 200)	
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
first_page = flask.Blueprint('first_page', __name__)
@first_page.route('/', methods=['GET'])
def show():
	#return flask.Response(data.db_name + '   ' + data.db_user, 200)	
	return flask.render_template('category.html',
				products = data.GetRNDProducts(),
				categories = None,				
				Current_Path = None,
				Current_Node = None
				)


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

edit_node_page = flask.Blueprint('edit_node_page', __name__)
@edit_node_page.route('/edit_cat/<cat_code>', methods=['GET'])
@requires_auth
def show(cat_code):
	return flask.render_template('frm_edit_node.html',
				Current_Path = data.GetCurrentPath(cat_code),
				Current_Node = data.GetCurrentNode(cat_code)
				)
				
@edit_node_page.route('/edit_cat/<cat_code>', methods=['POST'])
@requires_auth
def save(cat_code):
	new_name = flask.request.form['name']
	new_desc = flask.request.form['description']
	data.UpdateNode(cat_code, new_name, new_desc)
	return flask.redirect('/category/' + cat_code)

#########################################################################################

add_node_page = flask.Blueprint('add_node_page', __name__)
@add_node_page.route('/add_cat/<cat_code>', methods=['GET'])
@requires_auth
def show(cat_code):
	return flask.render_template('frm_add_node.html',
				Current_Path = data.GetCurrentPath(cat_code),
				Current_Node = data.GetCurrentNode(cat_code)
				)
				
@add_node_page.route('/add_cat/<cat_code>', methods=['POST'])
@requires_auth
@data.dbconnect
def save(cat_code):
	new_code = cat_code + '.' + flask.request.form['subcode']
	new_name = flask.request.form['name']
	new_desc = flask.request.form['description']
	data.SetNodeByCode(new_code, new_name, new_desc, True)
	return flask.redirect('/category/' + new_code)


#########################################################################################

edit_item_page = flask.Blueprint('edit_item_page', __name__)
@edit_item_page.route('/edit_item/<code>', methods=['GET'])
@requires_auth
def show(code):
	return flask.render_template('frm_edit_item.html',
				Current_Path = data.GetCurrentPath(code),
				item = data.GetCurrentProduct(code),
				price_list = data.GetProductPrices(code)
				)
				
@edit_item_page.route('/edit_item/<code>', methods=['POST'])
@requires_auth
def save(code):

	new_name = flask.request.form['name']
	new_desc = flask.request.form['description']
	new_cnt = int(flask.request.form['countOnStock'])
	
	# Цены
	p = float(flask.request.form['price_BIGOPT'])
	data.SetPrice(code, 'BIGOPT', p)

	p = float(flask.request.form['price_MIN'])
	data.SetPrice(code, 'MIN', p)
	p = float(flask.request.form['price_RETAIL'])
	data.SetPrice(code, 'RETAIL', p)

	data.UpdateProduct(code, new_name, new_desc, new_cnt)
	
	return flask.redirect('/product/' + code)
				
				
#########################################################################################

delete_item_page = flask.Blueprint('delete_item_page', __name__)
@delete_item_page.route('/delete_item/<code>', methods=['GET'])
@requires_auth
def show(code):
	return flask.render_template('frm_delete_item.html',
				Current_Path = data.GetCurrentPath(code),
				item = data.GetCurrentNode(code)
				)
				
@delete_item_page.route('/delete_item/<code>', methods=['POST'])
@requires_auth
def delete(code):
	item = data.GetCurrentNode(code)
	data.DeleteProduct(code)
	return flask.redirect('/category/' + item['parent'])
				
				
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
			
	order_id = data.MakeOrder(
		flask.request.form['org_name'],
		flask.request.form['user_name'],
		flask.request.form['user_mail'],
		flask.request.form['user_phone1'],
		flask.request.form['user_phone2'],
		flask.request.form['addr'],
		flask.request.form['remarks'],
		codes
		)
		
	# текст письма
	text = '<h3>123123123</h3><li>1<li>2'
	# заголовок письма
	subj = 'Заказ №%d' % order_id
	
	text = flask.render_template('order_letter.html',
					order = flask.request.form,
					products = data.GetOrderProducts(order_id)
					)
	data.send_mail(subj, text)	
#	return flask.Response(order_id, 200)
	return flask.render_template('base.html', content_name = 'content/thanks.html')

#########################################################################################
json_catalog_page = flask.Blueprint('json_catalog_page', __name__)
@json_catalog_page.route("/get_json_catalog", methods=['GET'] )
def get():
	dat = data.GetJsonTree()
	return flask.Response(json.dumps(dat), 200)
	
#########################################################################################
json_courses_page = flask.Blueprint('json_courses_page', __name__)
@json_courses_page.route("/get_json_courses", methods=['GET'] )
def get():
	dat = data.getCBR_Courses()
	return flask.Response(dat, 200)
	