__author__ = "Gondal, Saad Abdullah"
__version__ = "0.1"
__email__ = "saad-abdullah.gondal@capgemini.com"

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]
