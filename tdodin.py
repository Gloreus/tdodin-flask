# -*- coding: utf-8 -*- 

from flask import Flask, session, flash, redirect
from main import static_page
from main import cat_page



app = Flask(__name__)
app.debug = True

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect('/')
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	session['logged_in'] = True
	flash('You were logged in')
	return redirect('/')

app.register_blueprint(static_page) # /st_content/*
app.register_blueprint(cat_page) # /

# set the secret key.  keep this really secret:
app.secret_key = '$GL:KL:YR876TSDW#@#$'