from django.utils import timezone
from django.shortcuts import render
from django.views.generic.detail import DetailView

from cards.models import Card
from collection.models import CollectionEntry

class CardDetailView(DetailView):

    model = Card

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def CardsIndexView(request):
    """View function for cards index page."""

    # Generate counts of some of the main objects
    num_cards = Card.objects.all().count()
    num_entries = CollectionEntry.objects.all().count()

    # TODO add more counts of users, etc.

    context = {
        'num_cards': num_cards,
        'num_entries': num_entries
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'cards/card_index.html', context=context)
