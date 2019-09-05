from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from auth_app import models
# from auth_app.models import User


def validate_numeric ( value ):
    if not isnumeric( value ):
        raise ValidationError ( _('%(value)s is not a numeric value'), params = { 'value' : value }, )
    


def validate_mobile ( value ):
    is_numeric = validate_numeric ( value )
    
    if not is_numeric and len ( value ) != 11:
        raise ValidationError ( _('%(value)s is not a valid mobile number'), params = { 'value' : value }, )
   
   
     
def validate_maxlength ( value, max_length ):
    is_numeric = validate_numeric ( value )
    
    if not is_numeric and len ( value ) != max_length:
        raise ValidationError ( _('%(value)s must not be greater than %(max_length)'), params = { 'value' : value, 'max_length' : max_length }, )



def validate_minlength ( value, min_length):
    is_numeric = validate_numeric ( value )
    
    if not is_numeric and len ( value ) != min_length:
        raise ValidationError ( _('%(value)s must not be less than %(min_length)'), params = { 'value' : value, 'min_length' : min_length }, )
    
    
    
def validate_unique_email ( value ):
    try:
        user_email = models.User.objects.get( email = value)
        
        if user_email:
            raise ValidationError ( _('%(value) already exists in our database'), params = { 'value' : value }, )
        
    except models.User.DoesNotExist:
        return None