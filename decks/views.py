import re
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required

from decks.models import *
from collection.models import CollectionEntry
from decks.forms import DeckForm

class DeckDetailView(DetailView):

    model = Deck

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def DecksIndexView(request):
    """View function for decks index page."""

    # Generate counts of some of the main objects
    num_decks = Deck.objects.all().count()

    # TODO add more counts of users, etc.

    context = {
        'num_decks': num_decks
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'decks/deck_index.html', context=context)

@login_required
def add_deck(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DeckForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # TODO Save a new deck with the info provided in the form.
            # TODO load data from form.cleaned_data.

            # Create a new deck.
            deck = Deck.objects.create_deck(form.cleaned_data['deck_name'], request.user)

            # Import cards.
            if len(form.cleaned_data.get('deck_paste')) > 0:
                # TODO import cards from paste.
                data_lines = form.cleaned_data.get('deck_paste').splitlines()

                # Parse/validate lines.
                for num, line in enumerate(data_lines, start=1):
                    # Ensure line is in format <number> <string>.
                    if not re.match("^[0-9]+[\s]+.*", line):
                         # TODO throw error.
                         print("no match")
                    else:
                        # Grab quantity and card name.
                        # TODO add try/catch here.
                        split = line.split(" ", 1)
                        quantity = split[0]
                        card_name = split[1]

                        if quantity and card_name:
                            local_entry = Card.objects.filter(name__iexact=card_name)
                            if len(local_entry) > 0:
                                deck.cards.add(local_entry[0])

                deck.save()
            elif form.cleaned_data.get('deck_csv_upload'):
                # TODO import cards from csv.
                print("csv match")
            else:
                 # TODO throw error.
                 print("no match")

            # Import sideboard.
            if len(form.cleaned_data.get('sideboard_paste')) > 0:
                # TODO import cards from paste.
                print("no match")
            elif form.cleaned_data.get('sideboard_csv_upload'):
                # TODO import cards from csv.
                print("no match")
            else:
                raise forms.ValidationError(
                        # TODO add contact info
                        _('Something went wrong creating your sideboard.'),
                        code='error'
                    )

            # TODO process card lists.

            # Redirect to confirmation page

            return HttpResponseRedirect('/decks/' + str(deck.id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DeckForm()

    return render(request, 'decks/deck_form.html', {'form': form})
