from django.db import models
from django.contrib.auth.models import User
from decks.models import *

class Card(models.Model):
    # @See https://github.com/MagicTheGathering/mtg-sdk-python
    multiverseid = models.PositiveIntegerField(null=False, blank=False)
    name = models.CharField(max_length=200, unique=True)
    layout = models.CharField(max_length=50)
    mana_cost = models.CharField(max_length=10)
    cmc = models.PositiveIntegerField(null=False, blank=False)
    colors = models.TextField(null=False)
    color_identity = models.TextField(null=False)
    cardtype = models.TextField(null=False)
    supertypes = models.CharField(max_length=255)
    subtypes = models.CharField(max_length=255)
    rarity = models.CharField(max_length=255)
    text = models.TextField(null=False)
    flavor = models.TextField(null=False)
    number = models.PositiveIntegerField(null=False, blank=False)
    power = models.PositiveIntegerField(null=False, blank=False)
    toughness = models.PositiveIntegerField(null=False, blank=False)
    loyalty = models.PositiveIntegerField(null=False, blank=False)
    rulings = models.TextField(null=True)
    legalities = models.TextField(null=True)
    image_url = models.URLField(max_length=300, blank=True)
    set = models.CharField(max_length=255)
    set_name = models.TextField(null=True)
    printings = models.TextField(null=True)

    def __unicode__(self):
        return self.name

class CollectionEntry(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    owned = models.PositiveIntegerField(null=False, blank=False)
    wishlist = models.PositiveIntegerField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.card
