#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys


# По умолчанию используется версия Django 1.4.3,
# если вы хотите использовать другие версии, поменяйте эту переменную.
# Возможные значения: '1.4.3', '1.3', '1.2.3', '1.1.1'
# Если оставить строку пустой, будет использоваться версия, установленная на сервере.

# django_version = '1.4.3'

# Добавьте нужные вам пути поиска.
# Если вы получаете ошибку 500 Internal Server Error,
# скорее всего проблема именно в путях поиска.

activate_this = '/home/hosting_gloreus/PY/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, '/home/hosting_gloreus/projects/tdodin/app')
sys.path.insert(0, '/home/hosting_gloreus/projects/tdodin')

# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# ------ Ниже этой линии изменения скорее всего не нужны --------

python_lib = "python%d.%d" % (sys.version_info[0], sys.version_info[1])

# if django_version:
#     sys.path.insert(0, "/opt/django-%s/lib/%s/site-packages/" % (django_version, python_lib))

# import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

from tdodin import app as application
