from django.contrib import admin

from decks.models import (
    Deck,
    SideBoard
)

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    search_fields = ['name']

    # Ensure current user saves.
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(SideBoard)
class SideBoardAdmin(admin.ModelAdmin):
    list_display = ['deck']
    search_fields = ['deck']
