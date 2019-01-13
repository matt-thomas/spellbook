from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from cms.views import index

urlpatterns = [
  path('', index, name='index'),
]
