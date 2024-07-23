from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms.fields import Field
from django.forms.widgets import TextInput


class MultipleEmailField(Field):
    widget = TextInput
    default_validators = []
    default_error_messages = {
        'required': 'Default Required error message',
        'email': 'Please enter a valid email address or adrresses seperated by commas with no spaces'
    }

    # used to transform values to python objects
    def to_python(self, value):
        if not value:
            return []
        value = value.replace(' ', '')
        return value.split(',')
    
    def validate(self, value):
        for email in value:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError(self.error_messages['email'], code='email')
