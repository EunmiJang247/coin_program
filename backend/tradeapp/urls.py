from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
	path('send_telegram_message', send_telegram_message)
]