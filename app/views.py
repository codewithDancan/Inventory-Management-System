from django.shortcuts import render
from django.template.response import (TemplateResponse)

# Create your views here.
def home(request, year):
    print(type(year))
    print(year)
    return TemplateResponse(request, 'home.html', {'year': year})