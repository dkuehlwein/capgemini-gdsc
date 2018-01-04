from django.urls import *
from django.conf.urls import *

from . import views

urlpatterns = [
    #url(r'', views.search, name='search'),
    path('', views.search, name='search'),
    path('result/', views.result, name='search'),
    ]
