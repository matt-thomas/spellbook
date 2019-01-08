from django.db import models
from django.contrib.auth.models import User
from cards.models import Card

# Create your models here.
class CollectionEntry(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO add foil status.

    def __unicode__(self):
        return self.card