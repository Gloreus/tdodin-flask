# -*- coding: utf-8 -*- 

from flask import Flask, session, flash, redirect, request
import data
from main import static_page
from main import cat_page
from datetime import timedelta


app = Flask(__name__)
app.debug = True

import os

# читаем config

app.config.from_pyfile('/var/www/td-odin.cfg')
data.openDB(app.config['DB_NAME'], app.config['DB_USER'], app.config['DB_PASS'])

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('user_name', None) 
	session.pop('user_group', None)
	flash(u'Ждём Вас снова')
	return redirect('/')
	
@app.route('/login', methods=['POST'])
def login():
	user = request.form['login']
	password = request.form['password']
	user_info = data.auth_user(user, password)
	if user_info:
		session.permanent = True
		app.permanent_session_lifetime = timedelta(minutes=30)
		
		session['logged_in'] = True
		session['user_name'] = user_info['user_name']
		session['user_group'] = user_info['user_group']
	else:
		flash(u'Не знаю такого, ' + user + ' - ' + password)
	
	return redirect('/')

app.register_blueprint(static_page) # /st_content/*
app.register_blueprint(cat_page) # /


