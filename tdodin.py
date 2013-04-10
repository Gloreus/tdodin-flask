# -*- coding: utf-8 -*- 

from flask import Flask
from main import simple_page

app = Flask(__name__)
app.debug = True
app.register_blueprint(simple_page)
