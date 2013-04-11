# -*- coding: utf-8 -*- 

import MySQLdb as db

def GetTree():
# соединяемся с базой данных
	con = db.connect(host="localhost", user="root",
	     passwd="c300g", db="odin", charset='utf8')
	cur = con.cursor(db.cursors.DictCursor)
	cur.execute('select * from TreeItem')
	r = cur.fetchall()
	# закрываем соединение с БД
	con.close()
	return r