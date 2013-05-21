#-*- coding: utf-8 -*- 

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
		con = db.connect(host="mysql5.locum.ru", user=db_user, passwd=db_pass, db=db_name, charset='utf8')
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
def GetRNDProducts():
	price_type = flask.session.get('price_type')
	if not price_type:
		price_type = 'RETAIL'
	cur = con.cursor(db.cursors.DictCursor)
		
	sql = "call get_rnd_products('%s') " % price_type
	cur.execute(sql)
	q = cur.fetchall()
 	return q
	
@dbconnect	
def GetCategories(parent_code = '0'):
	cur = con.cursor(db.cursors.DictCursor)
	if parent_code == '0':
		sql = "select code, name from TreeItem t where t.is_node =1 and t.parent is null"
	else:	
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
def search(qstr):
	q = None
	if qstr and len(qstr) > 3:
		cur = con.cursor(db.cursors.DictCursor)
		
		sql = "select t.code, t.name from TreeItem t where t.is_node = 0 and upper(t.name) like '%" + qstr.upper() + "%'"
		cur.execute(sql)
		q = cur.fetchall()
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

@dbconnect	
def GetBasket():
	price_type = flask.session.get('price_type')
	if not price_type:
		price_type = 'RETAIL'
	ids = flask.request.cookies.get('basket')
	if not ids:
		return None
	ids = ids.strip('.')
	if ids == '':
		return None
	# из строк вида код-количество.код-количество. ....
	# выбираем код, переводим из hex в строку и склеиваем через запятую	
	ar_id = ["'" + s[:s.rfind('-')].decode('hex').replace("'", '"') + "'" for s in ids.split('.')]
	codes = ','.join(ar_id)
	codes = '(' + codes + ')'
	cur = con.cursor(db.cursors.DictCursor)
		
	cur.execute('call get_basket_by_codes("%s", "%s")' % (codes, price_type) )
	q = cur.fetchall()
	return q


@dbconnect	
def MakeOrder(
		org_name,
		user_name,
		email,
		user_phone1,
		user_phone2,
		address,
		remarks,
		codes):
	price_type = flask.session.get('price_type')
	if not price_type:
		price_type = 'RETAIL'
		
	cur = con.cursor()
	cur.execute("select add_order('%s', '%s', '%s', '%s','%s','%s','%s') as id" % (
		org_name,
		user_name,
		email,
		user_phone1,
		user_phone2,
		address,
		remarks)
		)
	q = cur.fetchone()
	order_id = q[0]
	for cod, cnt in codes:
		cur.execute("call add_order_product('%s', %d, '%s', %d) " % (price_type, order_id, cod.decode('hex'), cnt))
	con.commit()

	return q

@dbconnect
def GetClientInfo(order_id):
	cur = con.cursor(db.cursors.DictCursor)
	cur.execute("""
		SELECT
			id, org_name, user_name, email, user_phone1, user_phone2, address, remarks
		FROM odin.Orders o where o.id = %d
		""" % order_id)
	q = cur.fetchone()
	return q

@dbconnect
def GetOrderProducts(order_id):
	cur = con.cursor(db.cursors.DictCursor)
	cur.execute("""
			SELECT
				t.code, t.name, p.product_cnt as cnt, p.Ammount as amount
			FROM order_products p join TreeItem t on t.code = p.product_code
			WHERE p.order_id = %d
		""" % order_id)
	q = cur.fetchall()
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

def SetCount(cod, cnt):
	cur = con.cursor()
	try:
		cur.execute("UPDATE `TreeItem` t set t.countOnStock = %d WHERE t.code = '%s'" % (cnt, cod) )	
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

	if update_type == 'PRICE_REPLACE':
		update_type = 'PRICE_UPDATE'  # всё тоже самое, только не удаляем старые цены
		
	global Catalog
	Catalog = None
	book = xlrd.open_workbook(file_contents=xlsFile,  encoding_override='cp1251', formatting_info=True)
	sheet = book.sheet_by_index(0)
	
	if sheet.nrows < 3 or sheet.ncols < 3:
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
	
@dbconnect
def LoadCountsXLS(xlsFile):		
	s = u''	
	global Catalog
	Catalog = None
	book = xlrd.open_workbook(file_contents=xlsFile,  encoding_override='cp1251', formatting_info=True)
	sheet = book.sheet_by_index(0)
	
	if sheet.nrows < 9 or sheet.ncols < 3:
		return u'Error file structore!'
	
	s += u'Ostatki <hr>'
	
	# Первые 8 строк - шапка прайса
	for rnum in range(9, sheet.nrows):
		acaption = sheet.cell_value(rnum, 0).strip()
		acount = sheet.cell_value(rnum, 3)
		
		# Новые категории тут игнорируем
		if acount and acaption and type(acount) == float: 
		# Это строка товара
			# последнее слово - артикул должен быть
			acode = acaption[acaption.rfind(' ') + 1:]
			# Имя товара это всё между первым и последним пробелами
			# до первого пробела у нас краткий код
			# после последнего - артикул
			aname = acaption[: acaption.rfind(' ')]
			acode = acode.replace("'", '') # убрать кавычки если есть вдруг
			# Обновляем остатки на то, что уже есть
			if acode:
				SetCount(acode, round(acount) )
				s += str(rnum) + acode + ' = ' + str(acount) +   '<br>'
					
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
	
######################################################################################################
import smtplib
from email.MIMEText import MIMEText
def send_mail(mail_subj, mail_body):
	# отправитель
	me = 'site@td-odin.ru'
	# получатель
	addr = ['gloreus@gmail.com','odin@td-odin.ru','info@td-odin.ru']
	you = 'To: ' + ', '.join(addr)


	# SMTP-сервер
	server = 'smtp.gmail.com'
	port = 25
	user_name = 'site@td-odin.ru'
	user_passwd = 'photopassword'
	
	
	# формирование сообщения
	msg = MIMEText(mail_body,  _charset='utf-8', _subtype='html')
	msg['Subject'] = mail_subj
	msg['From'] = me
	msg['To'] = ', '.join(addr)

	# отправка
	s = smtplib.SMTP(server, port)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(user_name, user_passwd)
	s.sendmail(me, addr, msg.as_string())
	s.quit()