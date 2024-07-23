from django.template import Library
from app.models import MAKE_CHOICES

register = Library()

def vehicle_make(value):
    for i, choice in enumerate(MAKE_CHOICES):
        if i == value:
            try:
                return choice[1]
            except ValueError:
                pass