from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from cards.views import CardDetailView

urlpatterns = [
  url(r'^(?P<pk>\d+)$', CardDetailView.as_view(), name='card_details'),
]
