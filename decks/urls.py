from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from decks.views import DeckDetailView, DecksIndexView, add_deck

urlpatterns = [
  path('', DecksIndexView, name='deck_index'),
  path('add/', add_deck, name='deck_add'),
  url(r'^(?P<pk>.+)/$', DeckDetailView.as_view(), name='deck_details')
]
