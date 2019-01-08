from django.db import models
from django.contrib.auth.models import User
from cards.models import Card

class BuylistEntry(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO add foil status.

    def __unicode__(self):
        return self.card

class PricePull(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    # TODO add timestamp.
    # TODO add price value.
    # TODO add source info.

    def __unicode__(self):
        return self.card
