from django.contrib import admin

from cards.models import (
    Card
)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Card', {
            'fields': ('multiverse_id', 'image_url', 'name', 'cardtype', 'flavor', 'colors'),
        }),
        ('Mana', {
            'fields': ('mana_cost', 'cmc',),
        }),
        ('Stats', {
            'fields': ('power', 'toughness', 'loyalty',),
        }),
        ('Legality', {
            'classes': ('collapse',),
            'fields': (('legalities', 'rulings'),),
        }),
    )
    list_display = ('name', 'cardtype', 'cmc', 'power', 'toughness',)
    search_fields = ('name', 'cardtype')
