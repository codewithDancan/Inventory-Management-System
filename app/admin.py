from typing import Any
from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline
from django.contrib.auth.admin import UserAdmin
from django.http import HttpRequest
from .models import Vehicle, VehicleModel, Engine, Seller
from app1.forms import (VehicleForm, EngineModelForm, AddEngineModelForm,
                        EngineSuperUserForm)

# Register your models here.

class VehicleStackedInline(TabularInline):
    model = Vehicle
    extra = 2
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    list_display = [
            'vin', 'sold', 'price', 'make', 'vehicle_model', 'engine', 'image'
        ]
    list_filter = ['vin', 'price']
    list_display_links = ['make', 'vin', 'vehicle_model']
    list_edtable = ['price', 'image']
    list_per_page = 5
    ordering = ['sold']
    preserve_filters = False
    search_fields = ['vin']
    fields = ['vin', 'sold', 'price', 'make', 'vehicle_model', 'engine', 'image']
    # filter_horizontal = ['vin'] - must be a many to many field
    form = VehicleForm 
    radio_fields = {'engine': admin.HORIZONTAL}
    save_on_top = True
    '''prepopulated_fields = {
        'vehicle_model':('name', 'vin')
    }'''
    

admin.site.register(VehicleModel)

@admin.register(Engine)
class EngineAdmin(ModelAdmin):
    inlines = [VehicleStackedInline]

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any):
        if obj:
            if request.user.is_superuser:
                return EngineSuperUserForm
            return EngineModelForm
        else:
            return AddEngineModelForm
        
        return super(EngineAdmin,self).get_form(request, obj, **kwargs)
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any):
        print(obj.__dict__)
        return super().save_model(request, obj, form, change)
    
    def delete_model(self, request: HttpRequest, obj: Any):
        print(obj.__dict__)
        return super().delete_model(request, obj)
@admin.register(Seller)
class SellerAdmin(ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active']
    list_display_links = ['username', 'email']
