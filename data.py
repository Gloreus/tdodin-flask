# -*- coding: utf-8 -*- 

import MySQLdb as db
import hashlib
import flask

con = None
def openDB(db_name, db_user, db_pass):
	global con
	con = db.connect(host="localhost", user=db_user, passwd=db_pass, db=db_name, charset='utf8')
			
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
	
				
def GetTree():
# соединяемся с базой данных	
	cur = con.cursor(db.cursors.DictCursor)
	cur.execute('select * from TreeItem')
	q = cur.fetchall()
	# закрываем соединение с БД
	con.close()
	return q