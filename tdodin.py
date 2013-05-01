# -*- coding: utf-8 -*- 

from flask import Flask, session, request
import data
from main import *
from auth_util import login, logout
from datetime import timedelta
import sys

app = Flask(__name__)
app.debug = True

# читаем config
 
app.config.from_pyfile('td-odin.cfg')

data.db_name = app.config['DB_NAME']
data.db_user = app.config['DB_USER']
data.db_pass = app.config['DB_PASS']


@app.context_processor
def inject_catalog():
    return dict(
		tree=data.GetTree()
		)
		


#######################################################################
app.register_blueprint(first_page) # /		
app.register_blueprint(static_page) # /st_content/*
app.register_blueprint(category_page) # /category/1.2
app.register_blueprint(load_price_frm) # /load_file
app.register_blueprint(login) # /login
app.register_blueprint(logout) # /logout
app.register_blueprint(product_page) # /st_content/*
app.register_blueprint(load_images) # /load_images
app.register_blueprint(search_page) # /search
app.register_blueprint(basket_page) # /basket
app.register_blueprint(order_page) # /order
