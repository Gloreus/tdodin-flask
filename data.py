# -*- coding: utf-8 -*- 

import MySQLdb as db
import hashlib
import flask
import urllib2

Catalog = None
db_pass = ''
db_name = ''
db_user = ''

def dbconnect(func):
	def wrapper(*args, **kwargs):
		global con
		con = db.connect(host="localhost", user=db_user, passwd=db_pass, db=db_name, charset='utf8')
		res = func(*args, **kwargs)
		con.close()
		return res
	return wrapper

	
############################################################
			
@dbconnect
def auth_user(login, password):
	cur = con.cursor(db.cursors.DictCursor)
	m = hashlib.md5(password)
	pwd = m.hexdigest()
	cur.execute("""
				select user_name, user_group
				from site_users
				where login='%s' and password='%s'
		""" %(login, pwd) )
	q = cur.fetchone()
	return q

###########################################################	
@dbconnect	
def GetProducts(parent_code = ''):
	price_type = flask.session.get('price_type')
	if not price_type:
		price_type = 'RETAIL'
	cur = con.cursor(db.cursors.DictCursor)
		
	sql = "call get_products('%s', '%s') " % (parent_code, price_type)
	cur.execute(sql)
	q = cur.fetchall()
 	return q

@dbconnect	
def GetCategories(parent_code = ''):
	cur = con.cursor(db.cursors.DictCursor)
	sql = "select code, name from TreeItem t where t.is_node =1 and t.parent = '%s'" % parent_code
	cur.execute(sql)
	q = cur.fetchall()
 	return q
	
@dbconnect
def GetCurrentPath(code):
	q = None
	if code:
		cur = con.cursor(db.cursors.DictCursor)
		
		sql = "call  get_path_by_code('%s')" % code
		cur.execute(sql)
		q = cur.fetchall()
 	return q

@dbconnect
def GetCurrentNode(code):
	q = None
	if code:
		cur = con.cursor(db.cursors.DictCursor)
		
		sql = "select * from TreeItem t where t.code='%s'" % code
		cur.execute(sql)
		q = cur.fetchone()
 	return q

@dbconnect	
def GetCurrentProduct(code = ''):
	price_type = flask.session.get('price_type')
	if not price_type:
		price_type = 'RETAIL'
	cur = con.cursor(db.cursors.DictCursor)
		
	sql = "call get_product('%s', '%s') " % (code, price_type)
	cur.execute(sql)
	q = cur.fetchone()
	return q
	
################################################################
@dbconnect
def GetTree():
	def LoadTree(root = None):
		cur = con.cursor(db.cursors.DictCursor)
		if root is None:
			k = None
			s = u'<ul class="nav nav-list">'
		else:
			k = root
			s = u'<ul class="nav nav-list collapse'
			s += '" id="node_' + k.encode('hex').upper() + '">'

			
		sql = 'select name, code, hex(code) as hcode from TreeItem where is_node =1 and parent'
		if k:
			sql += "= '%s'" % k 
		else:
			sql += ' is null'
		sql += ' order by code'	
		cur.execute(sql)
		q = cur.fetchall()
		if not q:
			return u''

		for item in q:
			#ветви ниже этого узла
			subtree = LoadTree(item['code'])
			s += '<li><div>'

			if 	len(subtree) > 0:
				s += '<i class="icon-plus" data-toggle="collapse" data-target="#node_' + item['hcode'] + '"></i>'

			s += '<a href= "/category/' + item['code'] + '">' + item['name'] + '</a>'
			s += subtree + '</div>'
		s += '</ul>'
		return s

	global Catalog
	if Catalog is None:
		Catalog = LoadTree()
	return Catalog	

	

def clear_TreeItems():
	try:
		cur = con.cursor()
		cur.execute("truncate TreeItem")
		con.commit()
	except:
		con.rollback()
		return False
	return True

def clear_Prices(price_name):
	try:
		cur = con.cursor()
		cur.execute("delete from Price where price_name = '%s'" % price_name )
		con.commit()
	except:
		con.rollback()
		return False
	return True

def GetNodeByCode(cod, force_create=False):
	cur = con.cursor()
	try:
		cur.execute("select Get_Node_By_Code('%s',%d )" % (cod, int(force_create)) )	
		q = cur.fetchone()
		con.commit()
	except:
		con.rollback()
		return -1
	return q[0]

def SetNodeByCode(cod, name, desc, force_create=False):
	cur = con.cursor()
	try:
		cur.execute("select Set_Node_By_Code('%s','%s', '%s', %d )" % (cod, name, desc, int(force_create)) )	
		q = cur.fetchone()
		con.commit()
	except:
		con.rollback()
		return -1
	return q[0]

def SetProduct(cod, parent, name, desc, force_create=False):
	cur = con.cursor()
#	try:
	cur.execute("select Set_Product('%s', '%s', '%s', '%s', %d )"
			% (cod, parent, name.replace("'", '"'), desc.replace("'", '"'), int(force_create)) )	
	con.commit()
	# except:
		# con.rollback()
		# return -1
	return 1

def SetPrice(cod, price_type, price):
	cur = con.cursor()
	try:
		cur.execute("call Set_Price('%s', '%s', %d )" % (cod, price_type, price) )	
		con.commit()
	except:
		con.rollback()
		return -1
	return 1
	
def SetPhoto(cod, size, href, width, height):
	cur = con.cursor()
	try:
		cur.execute("call Set_Photo('%s', '%s', '%s', %d, %d)" % (cod, size, href, width, height) )	
		con.commit()
	except:
		con.rollback()
		return -1
	return 1
	
##########################################################################################
	
import xlrd
import re
	
@dbconnect
def LoadXLS(xlsFile, update_type, price_type):		
	s = u''	
	if update_type == 'FULL_REPLACE':
		clear_TreeItems()

	if update_type == 'PRICE_UPDATE':
		clear_Prices(price_type)
		
	global Catalog
	Catalog = None
	book = xlrd.open_workbook(file_contents=xlsFile,  encoding_override='cp1251', formatting_info=True)
	sheet = book.sheet_by_index(0)
	
	if sheet.nrows < 9 or sheet.ncols < 3:
		return u'Error file structore!'
	
	rcod = re.compile('^(\d[\d\.]*)\s')	#будем искать строки начинающие с одной или более цифр, это код раздела		
	root = ''
	cod = ''	
	s += update_type + '  |  ' + price_type + '<hr>'
	
	# Первые 2 строк - шапка прайса
	for rnum in range(2, sheet.nrows):
		acaption = sheet.cell_value(rnum, 1).strip()
		aprice = sheet.cell_value(rnum, 2)
		if aprice == '':
			aprice = 0
		
		# Новые категории подгружаем если меняем весь каталог
		if aprice == 0  and update_type != 'PRICE_UPDATE': 
			m = rcod.match(acaption)
			if m:
				cod1 = m.group(0).strip().strip('.')
				if cod1 != cod:			#Новый раздел
					root =  SetNodeByCode(cod1, acaption[m.end():].strip(), '', True)
					s += '<h2>' + cod1 +' | ' + acaption[m.end():].strip()  + '</h2>' 
					cod = cod1
					
		else:	# Это строка товара
			if aprice > 0:
				# последнее слово - артикул должен быть
				acode = acaption[acaption.rfind(' ') + 1:]
				if not acode:
					acode = acaption[:acaption.find(' ')]
				# Имя товара это всё между первым и последним пробелами
				# до первого пробела у нас краткий код
				# после последнего - артикул
				aname = acaption[: acaption.rfind(' ')]
				if update_type == 'PRICE_UPDATE': 
					# Обновляем цены на то, что уже есть
					SetPrice(acode, price_type, aprice)
					s += acode + ' ' + aname + ' $ ' + str(aprice) + '<br>'  
				else:	
					SetProduct(acode, root, aname, '', True)
					s += acode + ' ( ' + str(root) + ' )  ' + aname + '<br>'  
						
	return s
	
######################################################################################################

import json
@dbconnect
def LoadImages():
		# читаем заголовок и ищем путь к фоткам
		next_link = None
		res = u''
		h = {'Accept': 'application/json',
			'Content-Type':'application/json; charset=utf-8',
			'Accept-Charset': 'utf-8'}
		try: 
			req = urllib2.Request('http://api-fotki.yandex.ru/api/users/tdodin/', headers=h)
			feed = urllib2.urlopen(req).read()
			
			j = json.loads(feed)
			next_link = j['collections']['photo-list']['href']
			res  += u'<p>Открыли альбом.. ' + j['collections']['photo-list']['href']
		except Exception, inst:
			return res + str(inst)	
#		try:	
		while next_link:
			res += u'<p> читаем список фоток' + next_link		
			req = urllib2.Request(next_link, headers=h)
			feed = urllib2.urlopen(req).read()
			j = json.loads(feed)
			res += '<ul>'
			for e in j['entries']:	
				key = e['title']
				res += '<li>' + key
				key = key[:key.rfind('.')]
					
				res += '<ul>'
				img = e['img']
				for size in e['img']:
					res += '<li>' + size
					href = img.get(size)['href']
					width = img.get(size)['width']
					height = img.get(size)['height']
					res += ' | ' + img.get(size)['href']
					SetPhoto(key, size, href, width, height)
					
				res += '</ul>'	
			next_link = j['links'].get('next')	
			res += '</ul>'	
		return res + '<hr> All OK'		
#		except Exception, inst:
#			return res + str(inst)		
	