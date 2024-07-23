from django.urls import re_path, register_converter
from app.views import *
from django.views.generic import (TemplateView)

# from app1.converters import YearConverter


# register_converter(YearConverter, 'year')

urlpatterns = [
    re_path('app/(?P<year>[0-9]{4})/$', home),
]
