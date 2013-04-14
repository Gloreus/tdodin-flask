# -*- coding: utf-8 -*- 

from flask import Flask, session, flash, redirect, request
import data
from main import static_page
from main import cat_page


app = Flask(__name__)
app.debug = True

import os

# читаем config
app.config.from_pyfile('/var/www/td-odin.cfg')
app.secret_key = os.urandom(24)
data.openDB()

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect('/')
	
@app.route('/login', methods=['POST'])
def login():
	user = request.form['login']
	password = request.form['password']
	if data.auth_user(user, password):
		session['logged_in'] = True
		flash('You were logged in')
	return redirect('/')

app.register_blueprint(static_page) # /st_content/*
app.register_blueprint(cat_page) # /


