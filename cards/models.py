from django.db import models
from django.contrib.auth.models import User
from decks.models import *
from mtgsdk import Card as SDKCard

class CardManager(models.Manager):
    def create_card(self, number, set_code):
        # Use mtgsdk to lookup card info.
        cards = SDKCard.where(set=set_code).where(number=number).all()
        if len(cards) == 1:
            # Populate card info.
            import pdb
            pdb.set_trace()
            self.create(
                multiverse_id = cards[0].multiverse_id,
                name = cards[0].name,
                layout = cards[0].layout,
                mana_cost = cards[0].mana_cost,
                cmc = cards[0].cmc,
                colors = cards[0].colors,
                color_identity = cards[0].color_identity,
                cardtype = cards[0].type,
                supertypes = cards[0].supertypes,
                subtypes = cards[0].subtypes,
                rarity = cards[0].rarity,
                text = cards[0].text,
                flavor = cards[0].flavor,
                number = cards[0].number,
                power = cards[0].power,
                toughness = cards[0].toughness,
                loyalty = cards[0].loyalty,
                rulings = cards[0].rulings,
                legalities = cards[0].legalities,
                image_url = cards[0].image_url,
                set = cards[0].set,
                set_name = cards[0].set_name,
                printings = cards[0].printings
            )
        else:
            # TODO add error handling
            raise ValueError("oops! something went wrong with your lookup.")

class Card(models.Model):
    # @See https://github.com/MagicTheGathering/mtg-sdk-python
    multiverse_id = models.PositiveIntegerField(null=False, blank=False)
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
    loyalty = models.PositiveIntegerField(null=True, blank=True)
    rulings = models.TextField(null=True)
    legalities = models.TextField(null=True)
    image_url = models.URLField(max_length=300, blank=True)
    set = models.CharField(max_length=255, blank=False)
    set_name = models.TextField(null=True)
    printings = models.TextField(null=True)
    objects = CardManager()

    def __unicode__(self):
        return self.name
