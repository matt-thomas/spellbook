import re
from django.utils.translation import gettext as _
from django import forms

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
        self.errors = []

        # Ensure only one is uploaded.
        if len(self.cleaned_data.get('deck_paste')) > 1 and self.cleaned_data.get('deck_csv_upload'):
            self.errors.append(forms.ValidationError(
                    _('Please set only one deck import field: csv or paste'),
                    code='invalid'
                )
            )
        # If none are set, throw an error.
        elif len(self.cleaned_data.get('deck_paste')) == 0 and self.cleaned_data.get('deck_csv_upload') == None:
            self.errors.append(forms.ValidationError(
                    _('Please set one deck import field: csv or paste'),
                    code='invalid'
                )
            )

        # Ensure only one is provided.
        if len(self.cleaned_data.get('sideboard_paste')) > 1 and self.cleaned_data.get('sideboard_csv_upload'):
            self.errors.append(forms.ValidationError(
                    _('Please set only one sideboard import field: csv or paste'),
                    code='invalid'
                )
            )
        # If none are set, throw an error.
        elif len(self.cleaned_data.get('sideboard_paste')) == 0 and self.cleaned_data.get('sideboard_csv_upload') == None:
            self.errors.append(forms.ValidationError(
                    _('Please set one sideboard import field: csv or paste'),
                    code='invalid'
                )
            )

        if len(self.errors) > 0:
            raise forms.ValidationError(self.errors)

        # TODO Check each card in the import and ensure we have a relatable card.
        # Check cards import for deck.
        if len(self.cleaned_data.get('deck_paste')) > 0:
            self.parse_cards(self.cleaned_data.get('deck_paste'))
        elif self.cleaned_data.get('deck_csv_upload'):
            self.parse_csv(self.cleaned_data.get('deck_csv_upload'))
        else:
            raise forms.ValidationError(
                    # TODO add contact info
                    _('Something went wrong importing your deck.'),
                    code='error'
                )

        import pdb
        pdb.set_trace()

        # Check cards import for sideboard.
        if len(self.cleaned_data.get('sideboard_paste')) > 0:
            self.parse_cards(self.cleaned_data.get('sideboard_paste'))
        elif self.cleaned_data.get('sideboard_csv_upload'):
            self.parse_csv(self.cleaned_data.get('sideboard_csv_upload'))
        else:
            raise forms.ValidationError(
                        # TODO add contact info
                        _('Something went wrong importing your deck.'),
                        code='error'
                    )

    def parse_cards(self, card_data):
        data_lines = card_data.splitlines()

        # import pdb
        # pdb.set_trace()

        # Parse/validate lines.
        for num, line in enumerate(data_lines, start=1):
            # Ensure line is in format <number> <string>.
            if not re.match("^[0-9]+[\s]+.*", line):
                self.errors.append(forms.ValidationError(
                        # TODO add contact info
                        _('Invalid import line number %(num)s: "%(line)s" \n\n Lines must be in format <quantity> <card name>.'),
                        params={'num': num, 'line': line},
                        code='error'
                    )
                )
            else:
                # TODO grab <quantity> and <card name>
                # TODO use those params to query our local catalog of cards.
                # TODO if we find a local match, no worries.
                # TODO if we can't find a local match, query the cards.
                # TODO once harvester is done we'll substitute it here.
                quantity = re.match("^[0-9]+[\s]+", line)
                card_name = re.match("[\s]+.*", line)
                import pdb
                pdb.set_trace()

        # TODO write magic regex/util to turn pasted data into cards.
        self.errors.append(forms.ValidationError(
                        # TODO add contact info
                        _('I do not know how to import pasted data yet.'),
                        code='error'
                    )
        )

