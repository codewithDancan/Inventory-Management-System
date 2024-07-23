from django import forms
from image.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('caption', 'image')