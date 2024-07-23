from django.shortcuts import render, redirect
from image.forms import ImageForm
from image.models import *

# Create your views here.

def land(request):
    if request.method == 'POST':
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, 'land.html', {'obj': obj})
    else:
        form = ImageForm()
    img = Image.objects.all()
    return render(request, 'land.html', {'img': img, 'form': form})

