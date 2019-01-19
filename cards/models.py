import os
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from django.db import models
from django.contrib.auth.models import User
from mtgsdk import Card as SDKCard

class CardManager(models.Manager):
    def create_from_values(self, values):
        # Populate card info.
        self.create(
            multiverse_id = values['multiverse_id'],
            name = values['name'],
            layout = values['layout'],
            mana_cost = values['mana_cost'],
            cmc = values['cmc'],
            colors = values['colors'],
            color_identity = values['color_identity'],
            cardtype = values['cardtype'],
            supertypes = values['supertypes'],
            subtypes = values['subtypes'],
            rarity = values['rarity'],
            text = values['text'],
            flavor = values['flavor'],
            number = values['number'],
            power = values['power'],
            toughness = values['toughness'],
            loyalty = values['loyalty'],
            rulings = values['rulings'],
            legalities = values['legalities'],
            image_url = values['image_url'],
            set = values['set'],
            set_name = values['set_name'],
            printings = values['printings']
        )

    def create_card_lookup(self, number, set_code):
        # Use mtgsdk to lookup card info.
        cards = SDKCard.where(set=set_code).where(number=number).all()
        if len(cards) == 1:
            # Populate card info.
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
    multiverse_id = models.PositiveIntegerField(null=False, blank=False, primary_key=True)
    name = models.CharField(max_length=200, unique=False)
    layout = models.CharField(max_length=50)
    mana_cost = models.CharField(max_length=10, null=True, blank=True)
    cmc = models.PositiveIntegerField(null=True, blank=True)
    colors = models.TextField(null=False)
    color_identity = models.TextField(null=False)
    cardtype = models.TextField(null=False)
    supertypes = models.CharField(max_length=255)
    subtypes = models.CharField(max_length=255)
    rarity = models.CharField(max_length=255)
    text = models.TextField(null=True)
    flavor = models.TextField(null=True, blank=True)
    number = models.TextField(null=False, blank=False)
    power = models.PositiveIntegerField(null=True, blank=True)
    toughness = models.PositiveIntegerField(null=True, blank=True)
    loyalty = models.PositiveIntegerField(null=True, blank=True)
    rulings = models.TextField(null=True)
    legalities = models.TextField(null=True)
    image_url = models.URLField(max_length=300, blank=True)
    image_file = models.ImageField(upload_to='static/card_images/')
    set = models.CharField(max_length=255, blank=False)
    set_name = models.TextField(null=True)
    printings = models.TextField(null=True)
    objects = CardManager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # TODO confirm this isn't a duplicate of an existing card, if so abort.
        # Download image url into imagefield.
        if self.image_url and not self.image_file:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image_file.save(f"image_{self.multiverse_id}.png", File(img_temp))

        super(Card, self).save()
