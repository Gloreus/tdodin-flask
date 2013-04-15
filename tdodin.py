# -*- coding: utf-8 -*- 

from flask import Flask, session, flash, redirect, request
import data
from main import *
from auth_util import login, logout
from datetime import timedelta
import sys

# sys.path.insert(0, '/var/www/td-odin.ru/xlrd')

app = Flask(__name__)
app.debug = True

# читаем config

app.config.from_pyfile('/var/www/td-odin.cfg')
data.openDB(app.config['DB_NAME'], app.config['DB_USER'], app.config['DB_PASS'])

app.register_blueprint(static_page) # /st_content/*
app.register_blueprint(load_price_frm) # /load_file
app.register_blueprint(login) # /login
app.register_blueprint(logout) # /logout


