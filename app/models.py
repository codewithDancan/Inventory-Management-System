from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from django.db.models.functions import Lower
from django.contrib.auth.models import AbstractUser
from .manager import MercedesBenzManager, Ferari
from django.urls import reverse 


# Create your models here.
YESNO_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)
MAKE_CHOICES = (
    (1, 'Buick'),
    (2, 'Cadillac'),
    (3, 'Chevrolet'),
    (4, 'Jeep'),
)



class VehicleModel(models.Model):
    name = models.CharField(verbose_name='Model', max_length=100,
                             unique=True, blank=True, null=True)
    
    objects = models.Manager()

    ferari = Ferari()

    class Meta:
        verbose_name = 'Vehicle Model'
        verbose_name_plural = 'Vehicle Models'
        ordering = ['-name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields= ['-name'],
                         name='desc_name_idx'),
            models.Index(
                Lower('name').desc(),
                name = 'lower_name_idx'
            )
        ]
    def __str__(self) -> str:
        return self.name



class Engine(models.Model):
    name = models.CharField(verbose_name='Engine', max_length=100, unique=True, blank=True, null=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, verbose_name='Model',
                                      related_name='model_engine', blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
    
class engine2(models.Model):
    name = models.CharField(verbose_name='Engine', max_length=100, unique=True, blank=True, null=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, 
                                      verbose_name='Model', related_name='model_engine2',
                                      blank=True, null=True)
    
    class Meta:
        abstract = True
        db_table = 'Engine_Practice'
        ordering = ['name']
        verbose_name = 'Practise Engine'        
        verbose_name_plural = 'Practise Engines'  

class engine3(engine2):
    other_name = models.CharField(verbose_name='Other Engine Name',
                                  max_length = 75, blank = True, null=True)  
    

   



class Vehicle(models.Model):
    vin = models.CharField(verbose_name='VIN', max_length=50,  unique=True, blank=True, null=True)
    sold = models.BooleanField(verbose_name='Sold?', choices=YESNO_CHOICES, default=False, blank=True, null=True)
    price = MoneyField(max_digits=19, decimal_places=2, default_currency='KSH', null=True,
                       validators = [
                           MinMoneyValidator({'KSH': 500, 'USD': 5}),
                           MaxMoneyValidator({'KSH': 5000000, 'USD': 50000}),
                       ])
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, verbose_name='Model',
                                       related_name='model_vehicle', blank=True, null=True)
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE, verbose_name='Engine',
                               related_name='engine_vehicle', blank=True, null=True)
    make = models.PositiveBigIntegerField(choices=MAKE_CHOICES, verbose_name='Vehicle Make/Brand',
                                          blank=True, null=True)
    image = models.ImageField(upload_to='images')

    
    # default model manager 
    objects = models.Manager()

    # Mercedes Mananger
    mercedes_objects = MercedesBenzManager()

    def __str__(self):
        MAKE_CHOICES_DICT = dict(MAKE_CHOICES)
        return MAKE_CHOICES_DICT[self.make] + ' ' + str(self.vehicle_model)
    
    # custom model method 
    def full_vehicle_name(self):
        return self.__str__() + ' - ' + self.engine.name
    @property
    def full_name(self):
        return self.__str__() + ' - ' + self.engine.name
    
    def get_url(self):
        return reverse('vehicle_detail_view', kwargs={'id': self.pk})
        
    def get_absolute_url(self, request):
        base_url = request.build_absolute_uri('/') [:-1].strip('/')
        return base_url + reverse("vehicle_detail_view", kwargs={"id": self.pk})
    
    def natural_key(self):
        return self.full_vehicle_name()
    
    


class Seller(AbstractUser):
    name = models.CharField(verbose_name='Seller Name', max_length=150, blank=True, null=True)
    vehicle = models.ManyToManyField(Vehicle, verbose_name='Vehicles', related_name='vehicle_sellers', related_query_name='vehicle_seller', blank=True)
