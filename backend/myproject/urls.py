from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/trade/', include('tradeapp.urls'))
]
