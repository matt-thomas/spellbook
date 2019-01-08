from django.contrib import admin

from cards.models import (
    Card
)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('multiverse_id',),
        }),
        ('Card', {
            'fields': ('name', 'cardtype', 'rulings', 'flavor',),
        }),
        ('Mana', {
            'fields': ('mana_cost', 'cmc',),
        }),
        ('Stats', {
            'fields': ('power', 'toughness', 'loyalty',),
        }),
        ('Legality', {
            'classes': ('collapse',),
            'fields': (('legalities'),),
        }),
    )
    list_display = ('name', 'cardtype', 'cmc', 'power', 'toughness',)
    search_fields = ('name', 'cardtype')
