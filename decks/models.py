from django.db import models
from django.contrib.auth.models import User
from cards.models import Card
from cms.utils import unique_slugify

class DeckManager(models.Manager):
    def create_deck(self, name, user):
        deck = self.create(name=name, user=user)
        # do something with the deck
        return deck

class Deck(models.Model):
    name = models.CharField(max_length=200, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, editable=False)
    cards = models.ManyToManyField(Card, blank=True)
    objects = DeckManager()

    def __unicode__(self):
      return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, '%s' % (self.name))
        super(Deck, self).save()

class SideBoard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, blank=True)

    def __unicode__(self):
        return 'sideboard ' + self.deck
