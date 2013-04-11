# -*- coding: utf-8 -*- 

from flask import Flask
from main import static_page
from main import cat_page



app = Flask(__name__)
app.debug = True

app.register_blueprint(static_page) # /st_content/*
app.register_blueprint(cat_page) # /
