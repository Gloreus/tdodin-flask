# -*- coding: utf-8 -*- 
from flask import *
import data
from functools import wraps

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.<br>'
    'You have to login with proper credentials', 401,
    {})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		user_gr = session.get('user_group')
		if user_gr != 'ADMIN':
			return authenticate()
		return f(*args, **kwargs)
	return decorated


logout = Blueprint('logout', __name__)
@logout.route('/logout')
def show():
	session.pop('logged_in', None)
	session.pop('user_name', None)
	session.pop('user_group', None)
	flash(u'Ждём Вас снова')
	return redirect('/')
	
login = Blueprint('login', __name__)
@login.route('/login', methods=['POST'])
def show():
	user = request.form['login']
	password = request.form['password']
	user_info = data.auth_user(user, password)
	if user_info:
		session['logged_in'] = True
		session['user_name'] = user_info['user_name']
		session['user_group'] = user_info['user_group']
		flash(u'user ' + user_info['user_name'])
	else:
		flash(u'Не знаю такого, ' + user + ' - ' + password)
	return redirect('/')

