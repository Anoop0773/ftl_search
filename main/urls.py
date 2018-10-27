from django.urls import path,include
from main.views import *

urlpatterns = [
    path('', index),
    path('search', search, name='search'),
    
]