from django import forms

class DeckForm(forms.Form):
    deck_name = forms.CharField(label='Deck name', max_length=255)
    deck_csv_upload = forms.FileField(label='Deck CSV upload', required=False)
    deck_paste = forms.CharField(widget=forms.Textarea, label='Paste Deck', required=False, max_length=4096)
    sideboard_csv_upload = forms.FileField(label='Sideboard CSV upload', required=False)
    sideboard_paste = forms.CharField(widget=forms.Textarea, label='Paste Sideboard', required=False, max_length=4096)
    add_to_collection = forms.BooleanField(label='Add these cards to my collection?', required=False)

    def is_valid(self):
        # run the parent validation first
        valid = super(DeckForm, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        # TODO Ensure exactly one of csv and paste fields is set.
        # If two are set, throw an error.
        errors = True

        # Ensure only one is uploaded.
        if len(self.cleaned_data['deck_paste']) > 1 and self.cleaned_data['deck_csv_upload']:
          self._errors['too_many_inputs_deck'] = 'Please set only one: csv or paste'
          errors = True
        # If none are set, throw an error.
        elif len(self.cleaned_data['deck_paste']) == 0 and self.cleaned_data['deck_csv_upload'] == None:
          self._errors['too_few_inputs_deck'] = 'Please set one: csv or paste'
          errors = True

        # Ensure only one is provided.
        if len(self.cleaned_data['sideboard_paste']) > 1 and self.cleaned_data['sideboard_csv_upload']:
          self._errors['too_many_inputs_sideboard'] = 'Please set only one: csv or paste'
          errors = True
        # If none are set, throw an error.
        elif len(self.cleaned_data['sideboard_paste']) == 0 and self.cleaned_data['sideboard_csv_upload'] == None:
          self._errors['too_few_inputs_sideboard'] = 'Please set one: csv or paste'
          errors = True

        import pdb
        pdb.set_trace()

        # If we made it this far, return valid.
        return errors;
