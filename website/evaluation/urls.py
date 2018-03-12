from django.urls import *

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('result/', views.result, name='search'),
    re_path(r'^download/(?P<file_name>.+)$', views.download_file)
]
