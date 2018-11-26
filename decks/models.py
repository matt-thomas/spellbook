from django.db import models
from django.contrib.auth.models import User
from cards.models import Card

class Deck(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card)

    def __unicode__(self):
      return self.name

class SideBoard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card)

    def __unicode__(self):
        return 'sideboard ' + self.deck
