from django.db import models

class MercedesBenzManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(make=1)
    
class Ferari(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(name='Ferari')
    
