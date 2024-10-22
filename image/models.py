from django.db import models

# Create your models here.
class Image(models.Model):
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/%y')

    def __str__(self) -> str:
        return self.caption
