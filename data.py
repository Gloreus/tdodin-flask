# -*- coding: utf-8 -*- 

import MySQLdb as db
import hashlib

con = None
def openDB():
	global con
	con = db.connect(host="localhost", user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
			
def auth_user(login, password):
	cur = con.cursor()
	m = hashlib.md5(password)
	pas = m.hexdigest()
	cur.execute('select user_name from site_users where login=%s and password=%s', )
	q = cur.fetchone()
	if q:
		return q[0]
	else:
		return None
	
				
def GetTree():
# соединяемся с базой данных	
	cur = con.cursor(db.cursors.DictCursor)
	cur.execute('select * from TreeItem')
	q = cur.fetchall()
	# закрываем соединение с БД
	con.close()
	return q