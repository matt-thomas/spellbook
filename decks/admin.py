from django.contrib import admin

from decks.models import (
    Deck,
    SideBoard
)

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    search_fields = ['name']

@admin.register(SideBoard)
class SideBoardAdmin(admin.ModelAdmin):
    list_display = ['deck']
    search_fields = ['deck']
