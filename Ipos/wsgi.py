"""
WSGI config for Ipos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

import sys
import site

from django.core.wsgi import get_wsgi_application

sys.path.append('C:/Users/MY PC/AppData/Local/Programs/Python/Python39')
sys.path.append('C:/Users/MY PC/AppData/Local/Programs/Python/Python39')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Ipos.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ipos.settings')

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ipos.settings')

application = get_wsgi_application()
