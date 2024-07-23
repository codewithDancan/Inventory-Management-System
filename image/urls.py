from django.urls import path
from image.views import land


urlpatterns = [
    path('land/', land, name='land'),
]
