from django.utils import timezone
from django.views.generic.detail import DetailView

from cards.models import Card

class CardDetailView(DetailView):

    model = Card

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
