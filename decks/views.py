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

            # TODO process card lists.

            # Redirect to confirmation page

            return HttpResponseRedirect('/decks/add/thanks?did=')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DeckForm()

    return render(request, 'decks/deck_form.html', {'form': form})
