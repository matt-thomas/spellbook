import re
from django.utils.translation import gettext as _
from django import forms
from cards.models import Card
from mtgsdk import Card as SDKCard

class DeckForm(forms.Form):
    deck_name = forms.CharField(label='Deck name', max_length=255)
    deck_csv_upload = forms.FileField(label='Deck CSV upload', required=False)
    deck_paste = forms.CharField(widget=forms.Textarea, label='Paste Deck', required=False, max_length=4096)
    sideboard_csv_upload = forms.FileField(label='Sideboard CSV upload', required=False)
    sideboard_paste = forms.CharField(widget=forms.Textarea, label='Paste Sideboard', required=False, max_length=4096)
    add_to_collection = forms.BooleanField(label='Add these cards to my collection?', required=False)

    def clean(self):
        # Run parent
        cleaned_data = super().clean()

        # TODO Ensure exactly one of csv and paste fields is set.
        # If two are set, throw an error.
        errors = []

        # Ensure only one is uploaded.
        if len(self.cleaned_data.get('deck_paste')) > 1 and self.cleaned_data.get('deck_csv_upload'):
            errors.append(forms.ValidationError(
                    _('Please set only one deck import field: csv or paste'),
                    code='invalid'
                )
            )
        # If none are set, throw an error.
        elif len(self.cleaned_data.get('deck_paste')) == 0 and self.cleaned_data.get('deck_csv_upload') == None:
            errors.append(forms.ValidationError(
                    _('Please set one deck import field: csv or paste'),
                    code='invalid'
                )
            )

        # Ensure only one is provided.
        if len(self.cleaned_data.get('sideboard_paste')) > 1 and self.cleaned_data.get('sideboard_csv_upload'):
            errors.append(forms.ValidationError(
                    _('Please set only one sideboard import field: csv or paste'),
                    code='invalid'
                )
            )
        # If none are set, throw an error.
        elif len(self.cleaned_data.get('sideboard_paste')) == 0 and self.cleaned_data.get('sideboard_csv_upload') == None:
            errors.append(forms.ValidationError(
                    _('Please set one sideboard import field: csv or paste'),
                    code='invalid'
                )
            )

        # check here for errors. we don't want to proceed if so.
        if len(errors) > 0:
            raise forms.ValidationError(errors)

        # TODO Check each card in the import and ensure we have a relatable card.
        # Check cards import for deck.
        if len(self.cleaned_data.get('deck_paste')) > 0:
            errors += self.parse_cards(self.cleaned_data.get('deck_paste'))
        elif self.cleaned_data.get('deck_csv_upload'):
            errors += self.parse_csv(self.cleaned_data.get('deck_csv_upload'))
        else:
            raise forms.ValidationError(
                    # TODO add contact info
                    _('Something went wrong importing your deck.'),
                    code='error'
                )

        # Check cards import for sideboard.
        if len(self.cleaned_data.get('sideboard_paste')) > 0:
            errors += self.parse_cards(self.cleaned_data.get('sideboard_paste'))
        elif self.cleaned_data.get('sideboard_csv_upload'):
            errors += self.parse_csv(self.cleaned_data.get('sideboard_csv_upload'))
        else:
            raise forms.ValidationError(
                        # TODO add contact info
                        _('Something went wrong importing your deck.'),
                        code='error'
                    )

        if len(errors) > 0:
            raise forms.ValidationError(errors)

    def parse_cards(self, card_data):
        data_lines = card_data.splitlines()

        errors = []

        # Parse/validate lines.
        for num, line in enumerate(data_lines, start=1):
            # Ensure line is in format <number> <string>.
            if not re.match("^[0-9]+[\s]+.*", line):
                errors.append(forms.ValidationError(
                        # TODO add contact info
                        _('Invalid import line number %(num)s: "%(line)s" \n\n Lines must be in format <quantity> <card name>.'),
                        params={'num': num, 'line': line},
                        code='error'
                    )
                )
            else:
                # Grab quantity and card name.
                # TODO add try/catch here.
                split = line.split(" ", 1)
                quantity = split[0]
                card_name = split[1]

                if quantity and card_name:
                    # Search local catalog for card.
                    local_entry = Card.objects.filter(name=card_name)

                    # If we find a local match, no worries.
                    if len(local_entry) > 0:
                        return
                    else:
                        # If we can't find a local match, query the card api.
                        cards = SDKCard.where(name=card_name).all()
                        if len(cards) > 0:
                            # TODO If we find cards, create them all locally.
                            for card in cards:
                                if card.multiverse_id:
                                    values = {
                                        "multiverse_id": card.multiverse_id,
                                        "name": card.name,
                                        "layout": card.layout,
                                        "mana_cost": card.mana_cost,
                                        "cmc": card.cmc,
                                        "colors": card.colors,
                                        "color_identity": card.color_identity,
                                        "cardtype": card.type,
                                        "supertypes": card.supertypes,
                                        "subtypes": card.subtypes,
                                        "rarity": card.rarity,
                                        "text": card.text,
                                        "flavor": card.flavor,
                                        "number": card.number,
                                        "power": card.power,
                                        "toughness": card.toughness,
                                        "loyalty": card.loyalty,
                                        "rulings": card.rulings,
                                        "legalities": card.legalities,
                                        "image_url": card.image_url,
                                        "set": card.set,
                                        "set_name": card.set_name,
                                        "printings": card.printings
                                    }
                                    Card.objects.create_from_values(values)
                                else:
                                    errors.append(forms.ValidationError(
                                            # TODO add contact info
                                            _('Invalid import line number %(num)s: "%(line)s" \n\n Could not find card multiverse ID.'),
                                            params={'num': num, 'line': line},
                                            code='error'
                                        )
                                    )
                        else:
                            errors.append(forms.ValidationError(
                                    # TODO add contact info
                                    _('Invalid import line number %(num)s: "%(line)s" \n\n Could not find matching card name.'),
                                    params={'num': num, 'line': line},
                                    code='error'
                                )
                            )
                else:
                    errors.append(forms.ValidationError(
                            # TODO add contact info
                            _('Invalid import line number %(num)s: "%(line)s" \n\n Could not understand this line.'),
                            params={'num': num, 'line': line},
                            code='error'
                        )
                    )

        # Return any errors we've generated.
        return errors

