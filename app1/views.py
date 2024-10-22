from django.shortcuts import render
from django.template.response import (TemplateResponse)
from django.http import (
    Http404,
      HttpRequest,
        HttpResponse, 
            HttpResponseRedirect,
                JsonResponse,
        ) 

from app.models import *


from django.views import View

from .forms import(ContactForm,
                    VehicleForm,
                      VehicleModelForm,
                        EngineModelForm,
                          ProspectiveBuyerFormSet) 
from django.views.generic.edit import (FormView,
                                        CreateView,
                                          UpdateView)
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from django.contrib import messages
from django.core.mail import EmailMessage
from .email import send_email
from django.conf import settings
# from .pdf import generate_pdf

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    EngineSerializer, 
    VehicleSerializer, 
    VehicleModelSeerializer, 
    SellerSerializer
)
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import logging


# Create your views here.

def practice_view(request, year):
    print(
        request.build_absolute_uri(reverse(
            'year_url', args=(2023,)
        ))
    )
    print(
        request.build_absolute_uri(reverse(
            'year_url', args=(2024,)
        ))
    )
   
    return TemplateResponse(request, 'practice.html', {'year': year})
def practice_year_view(request, year):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info("The requested year is: %s % year")
    if year >=2020:
        print(type(year))
        print(year)

        return TemplateResponse(request, 'year.html', {'year': year})
    else:
        raise Http404(f'Input a year Greater or equal to 2020: {year}')
    
class VehicleListView(View):
    template_name = 'vehicle.html'
    def get(self, request, *args, **kwargs):
        other_vehicles = Vehicle.objects.prefetch_related("vehicle_sellers").select_related("vehicle_model", "engine").all()
        return TemplateResponse(request, self.template_name, {'other_vehicles': other_vehicles})
        


class VehicleDetailView(View):
    template_name = 'vehicle-detail.html'
    def get(self, request, id):
        try:
            current_vehicle = Vehicle.objects.get(id=id)
            
        except Vehicle.DoesNotExist:
            raise Http404(f'Vehicle with ID of {id} not found')
        else:
            print(current_vehicle.get_url())
            print(current_vehicle.get_absolute_url(request))
        return TemplateResponse(request, self.template_name,
                                {'current_vehicle': current_vehicle})
    
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect('/success/')
    
class TestPageView(View):
    template_name = 'test.html'
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name, {
            'title': 'Caching in Django',
            'body': 'I am a backend engineer',
        })
class FormClassView(FormView):
    template_name = 'form-class.html'
    form_class = ContactForm
    success_url = 'contact-form-success/'

    def get(self, request, *args, **kwargs):
        initial = {
            'full_name': 'FirstName LastName',
            'email_1': 'example@gmail.com',
        }
        return TemplateResponse(request, self.template_name, {
            'title': 'FormClassView Page',
            'page_id': 'form-class-id',
            'page_class': 'form-class-page',
            'h1_tag': 'This is the FormClassView Page Using ContactForm',
            'form': self.form_class(initial),
        })
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.add_message(request, 
                                 messages.SUCCESS, "Your contact form submitted successfully", extra_tags="bold", fail_silently=True)
        else:
            messages.add_message(request, 
                                 messages.ERROR, "There was a problem in submitting your contact form")
            
        context = {
                'title': 'FormClassView Page - Please Correct The Errors Below',
                'page_id': 'form-class-id',
                'page_class': 'form-class-page errors-found',
                'h1_tag': 'This is the FormClassView Page Using ContactForm<br /><small class="error-msg">Errors Found</small>',
                'form': form,
                
            }
        return TemplateResponse(request, self.template_name, context)


class VehicleFormCreateView(CreateView):
    model = Vehicle
    template_name = 'vehicle-form.html'
    form_class = VehicleForm
    success_url = reverse_lazy('vehicle-form-success')

    """def send_email(self, request):
        data = self.cleaned_data
        msg_body = "New Vehicle created Successfully"
        email = EmailMessage(
            subject="New Vehicle Entry",
            body=msg_body,
            from_email="codewithdancan@gmail.com",
            reply_to= "ngagadancan2003@gmail.com",
            cc = [],
            bcc = [],
            to= [data["email_1"]],
            attachments= [], 
            headers= {},
        )
        email.content_subtype = "plain"
        email.send()"""

    def get(self, request, *args,  **kwargs):
        buyer_formset = ProspectiveBuyerFormSet()
        return TemplateResponse(request, self.template_name, { 'form': self.form_class(),
                                                              'buyer_formset': buyer_formset})
    
    def post(self, request):
        form = self.form_class(request.POST, files=request.FILES)

        buyer_formset = ProspectiveBuyerFormSet(request.POST)

        try:
            if form.is_valid():
                messages.add_message(request, messages.SUCCESS, "Your Vehicle has been successfully created",
                                 fail_silently=True, extra_tags="bold")
            else:
                messages.add_message(request, messages.ERROR, "Error in creating your vehicle", extra_tags="bold")

            vehicle = form.instance
            vehicle.save()
            # send_email(self, request)
            #generate_pdf()
            return HttpResponseRedirect(reverse("vehicle-view"))
        except ValidationError:
            return TemplateResponse(request, self.template_name, {'form': form, 'buyer-formset': buyer_formset})
       
    
class VehicleModelFormCreateView(CreateView):
    model = VehicleModel
    template_name = 'vehicle-model-form.html'
    form_class = VehicleModelForm

    def get(self, request):
        return TemplateResponse(request, self.template_name, {'form': self.form_class()})
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            vehicle_model = form.instance
            vehicle_model.save()
            return render(request, 'vehicle-model-form-success.html')
        else:
            return TemplateResponse(request, self.template_name, {'form': form})
        
class EngineCreateView(CreateView):
    model = Engine
    template_name = 'engine-form.html'
    form_class = EngineModelForm

    def get(self, request):
        return TemplateResponse(request, self.template_name, {'form': self.form_class()})
    
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            engine = form.instance
            engine.save()
            return render(request, 'engine-form-success.html')
        else:
            return TemplateResponse(request, self.template_name, {'form': form})
        
class VehicleFormUpdateView(UpdateView):
    model = Vehicle
    template_name = 'vehicle-form-update.html'
    form_class = VehicleForm
    success_url = '/vehicle-form-success/'

    def get(self, request, id, *args, **kwargs):
        try:
            vehicle = Vehicle.objects.get(id=id)
        except Vehicle.DoesNotExist:
            form = self.form_class()
        else:
            form = self.form_class(instance=vehicle)
        return TemplateResponse(request, self.template_name, {'form': form})
    
    def post(self, request, id, *args, **kwargs):
        form = self.form_class(request.POST, files=request.FILES)

        if form.is_valid():
            vehicle=form.instance
            vehicle.save()
            return redirect('vehicle')
        else:
            return TemplateResponse(request, self.template_name, {'form': form})
        
class VehicleModelFormUpdateView(UpdateView):
    model = VehicleModel
    template_name = 'vehicle-model-update.html'
    form_class = VehicleModelForm

    def get(self, request, id, *args, **kwargs):
        try:
            vehicle_model = VehicleModel.objects.get(id=id)
        except VehicleModel.DoesNotExist:
            form = self.form_class()
        else:
            form = self.form_class(instance=vehicle_model)
        return TemplateResponse(request, self.template_name, {'form': form})
    def post(self, request, id, *args, **kwargs):
        form = self.form_class(request.POST, files=request.FILES)
        if form.is_valid():
            vehicle_model = form.instance
            vehicle_model.save()
            return redirect('vehicle_view')
        else:
            return TemplateResponse(request, self.template_name, {'form': form})
        
class EngineViewSet(ModelViewSet):
    queryset = Engine.objects.all().order_by("name")
    serializer_class = EngineSerializer
    permission_classes = [IsAuthenticated]

class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all().order_by("vin")
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

class VehicleModelViewSet(ModelViewSet):
    queryset = VehicleModel.objects.all().order_by("name")
    serializer_class = VehicleModelSeerializer
    permission_classes = [IsAuthenticated]

class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]


class GetSellerView(View):
    template_name = "get-seller.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return TemplateResponse(request, self.template_name, context)
    
class GetSellerHTMLView(APIView):
    permission_classes = [IsAuthenticated]
    template_name = "seller.html"


    def get(self, request, format=None, id=0, *args, **kwargs):
        if request.user.is_authenticated and request.user.has_perm("view_user"):
            try:
                seller = Seller.objects.get(id=id)
            except seller.DoesNotExist:
                seller = None
        else:
            seller = None
        context = {"seller": seller}
        return render(request, self.template_name, context=context)
class GetSellerWithTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, id=0, *args, **kwargs):
        seller = None
        req_user = request._user

        if req_user.has_perm("view_user"):
            perm_granted = True
            try:
                seller = Seller.objects.get(id=id)
            except seller.DoesNotExist:
                pass
        else:
            perm_granted = False

        context = {
                "request": request,
                "seller": seller,
            }

        seller = SellerSerializer(seller, context=context)

        new_context = {
                "seller": seller.data,
                "perm_granted": perm_granted
            }
        return JsonResponse(new_context)
    

class SellersView(View):
    template_name = "sellers.html"

    def get(self, request, *args, **kwargs):
        try:
            sellers = Seller.objects.prefetch_related("vehicle", "vehicle__vehicle_model", "vehicle__engine").all()
        except sellers.DoesNotExist:
            raise Http404("No Sellers Found")
        return TemplateResponse(request, self.template_name, {"sellers": sellers})




