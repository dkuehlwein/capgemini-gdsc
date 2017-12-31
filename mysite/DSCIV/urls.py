from django.urls import *
from django.conf.urls import *

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('?businessquery=$', views.search, name='search'),
    ]
