from django.shortcuts import render
from cards.models import Card

def index(request):
    """View function for home page of site."""

    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'cms/index.html', context=context)

