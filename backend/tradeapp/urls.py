from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
	path('open_long_position', open_long_position)
]