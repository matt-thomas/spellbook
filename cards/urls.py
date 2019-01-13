from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from cards.views import CardDetailView, CardsIndexView

urlpatterns = [
  path('', CardsIndexView, name='card_index'),
  url(r'^(?P<pk>\d+)$', CardDetailView.as_view(), name='card_details'),
]
