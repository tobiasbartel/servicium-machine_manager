__author__ = 'tbartel'
from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^(?P<my_instance_name>[\w-]+)/graph/$', machine_graph),
]