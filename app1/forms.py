from django.forms import Form, ModelForm, formset_factory
from django import forms
from django.core.validators import EmailValidator, validate_email
from django.core.exceptions import ValidationError
from .fields import MultipleEmailField
from app.models import Vehicle, VehicleModel, Engine

class ContactForm(Form):
    full_name = forms.CharField(label='Full Name', help_text='Enter your first and last name',
                                min_length=2, max_length=300, required=True, 
                                error_messages= {
                                    'required': 'Please provide us with your name',
                                    'min_length': 'Please provide a name with a minimum of 2 characters', 
                                    'max_length': 'Please provide a name with a minimum of 300 characters', 
                                })
    widget = forms.TextInput(
        attrs={
            'id': 'full-name',
            'class': 'form-input-class',
            'placeholder': 'Your name'
        }
    )
    email = forms.CharField(label='Email address',
                            min_length=5, max_length=300, required=False,
                            help_text='Email address-example@gmail.com',
                            validators= [
                                EmailValidator('Please enter a valid email address'),
                            ], error_messages= {
                                    'min_length': 'Please provide a name with a minimum of 5 characters', 
                                    'max_length': 'Please provide a name with a minimum of 300 characters', 
                                })
    email_2 = forms.EmailField(label='Email address', min_length=5, max_length=300, required=True,
                               help_text='Email adreess - example@gmail.com')

    email_3 = forms.CharField(label='Email using clean method',
                               required=False,
                                 help_text='Email address - example@gmail.com')
    conditional_required = forms.CharField(label='Required only if field labeled "email_3" has a value',
                                           help_text='Required only if field labeled "email_3" has a value', 
                                           required=False)
    multiple_emails = MultipleEmailField(label='Multiple email field',
                                         help_text='Please enter one or more email adsresses, each separated by a comma with no spaces',
                                         required=True)

    def clean_email_3(self):
        email = self.cleaned_data['email_3']
        if email != '':
            try:
                validate_email(email)
            except ValidationError:
                self.add_error('email_3', 'This field is required')
        else:
            return email
    def clean(self):
        email = self.cleaned_data['email_3']
        text_field = self.cleaned_data[
                                       'conditional_required']
        if email and not text_field:
            self.add_error(
                'conditional_required', 'if there is a value in the field labeled "email_3" then this field is required'
            )


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vin', 'sold', 'price', 'make', 'vehicle_model', 'engine', 'image'
        ]
class VehicleModelForm(ModelForm):
    class Meta:
        model = VehicleModel
        fields = [
            'name'
        ]

class EngineModelForm(ModelForm):
    class Meta:
        model = Engine
        fields = ['name', 'vehicle_model']
class AddEngineModelForm(ModelForm):
    class Meta:
        model = Engine
        fields = ['name', 'vehicle_model']
class EngineSuperUserForm(ModelForm):
    class Meta:
        model = Engine
        fields = ['name', 'vehicle_model']

class ProspectiveBuyerForm(Form):
    first_name = forms.CharField(label='First Name', help_text='Enter your First Name',
                                 required=True, error_messages={
                                     'required': 'Please provide us with a first name',
                                 })
    last_name = forms.CharField(label='Last Name', help_text='Enter your Last Name',
                                 required=True, error_messages={
                                     'required': 'Please provide us with a last name',
                                 })
    
ProspectiveBuyerFormSet = formset_factory(ProspectiveBuyerForm, extra=1)

