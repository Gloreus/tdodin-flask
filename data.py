# -*- coding: utf-8 -*- 

import MySQLdb as db
import hashlib
import flask

con = None
Catalog = None

def openDB(db_name, db_user, db_pass):
	global con
	con = db.connect(host="localhost", user=db_user, passwd=db_pass, db=db_name, charset='utf8')

############################################################
			
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
def GetTree():
# соединяемся с базой данных	
	cur = con.cursor(db.cursors.DictCursor)
	cur.execute('select * from TreeItem')
	q = cur.fetchall()
	# закрываем соединение с БД
	return q

def GetTree():
	global Catalog
	if Catalog is None:
		Catalog = LoadTree()
	return Catalog

def LoadTree(root = None):

	if root is None:
		k = None
		s = u'<ul class="nav nav-list">'
	else:
		k = root
		s = u'<ul class="nav nav-list collapse'
		s += '" id="node_' + str(k) + '">'

	cur = con.cursor(db.cursors.DictCursor)
		
	sql = 'select id, name from TreeItem where is_node =1 and parent'
	if k:
		sql += '= ' + str(k)
	else:
		sql += ' is null'
	sql += ' order by code'	
	cur.execute(sql)
	q = cur.fetchall()
	if not q:
		return u''

	for item in q:
		#ветви ниже этого узла
		subtree = LoadTree(item['id'])
		s += '<li><div>'

		if 	len(subtree) > 0:
			s += '<i class="icon-plus" data-toggle="collapse" data-target="#node_' + str(item['id']) + '"></i>'

		s += '<a href= "/category/' + str(item['id']) + '">' + item['name'] + '</a>'
		s += subtree + '</div>'
	s += '</ul>'
	return s
	
	
	
	
def clear_TreeItems():
	try:
		cur = con.cursor()
		cur.execute("truncate TreeItem")
	except:
		return False
	return True

def clear_Prices(price_name):
	try:
		cur = con.cursor()
		cur.execute("delete from Price where price_name = '%s'" % price_name )
	except:
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
	try:
		cur.execute("select Set_Product('%s', %d, '%s', '%s', %d )" % (cod, parent, name, desc, int(force_create)) )	
		q = cur.fetchone()
		con.commit()
	except:
		con.rollback()
		return -1
	return q[0]

def SetPrice(cod, price_type, price):
	cur = con.cursor()
	try:
		cur.execute("select Set_Price('%s', '%s', %d )" % (cod, price_type, price) )	
		q = cur.fetchone()
		con.commit()
	except:
		con.rollback()
		return -1
	return q[0]
	
##########################################################################################
	
import xlrd
import re
	
def LoadXLS(xlsFile, update_type, price_type):		
	if update_type == 'FULL_REPLACE':
		clear_TreeItems()

	if update_type == 'PRICE_UPDATE':
		clear_Prices(price_type)
		
	book = xlrd.open_workbook(file_contents=xlsFile,  encoding_override='cp1251', formatting_info=True)
	sheet = book.sheet_by_index(0)
	
	if sheet.nrows < 9 or sheet.ncols < 3:
		return u'Error file structore!'
	
	s = u''	
	
	
	rcod = re.compile('^(\d[\d\.]*)\s')	#будем искать строки начинающие с одной или более цифр, это код раздела		
	root = 0
	cod = ''	
	
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
				else:	
					SetProduct(acode, root, aname, '', True)
					s += acode + ' ( ' + str(root) + ' )  ' + aname + '<br>'  
						
	return s