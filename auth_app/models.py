from django.db import models
from django.urls import reverse
from django.utils import timezone
from main_app.models import Location
from django.core.validators import validate_email

from django.contrib.auth.models import ( 
    BaseUserManager, AbstractBaseUser 
)

from auth_app.validation import (
    validate_numeric, 
    validate_mobile, 
    validate_maxlength, 
    validate_minlength,
    validate_unique_email,
)

# Create your models here.
class UserManager ( BaseUserManager ):
    def create_user ( self, email, first_name, last_name, password = None ):
        if not email:
            raise ValueError( 'Email is required' )
        
        if not full_name:
            raise ValueError('First name is required')
        
        if not last_name:
            raise ValueError('Last name is required')
        
        user = self.model(
            email = self.normalize_email( email ),
        )
        
        user.first_name = first_name
        user.last_name = last_name
        user.password = password
        user.date_of_birth = timezone.localdate()
        
        user.set_password( password )
        user.save( using = self._db )
        return user
    
    def create_superuser ( self, email, first_name, last_name, password = None ):
        user = self.create_user(
            email = email,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        
        user.is_admin = True
        user.save( using = self._db )        
        return user



class User ( AbstractBaseUser ):
    # I am overriding most of the fields in the AbstractBaseUser class
    # to set their config to my application's specific tastes
    MALE = 'M'
    FEMALE = 'F'
    
    ADMIN = 'A'
    LANDLORD = 'L'
    TENANT = 'T'
    VENDOR = 'V'
    
    GENDER = (
        ( MALE, 'Male' ),
        ( FEMALE, 'Female' ),
    )
    
    USER_TYPE = (
        ( LANDLORD, 'Landlord' ),
        ( TENANT, 'Tenant' ),
        ( VENDOR, 'Vendor' ),
    )

    # I set the max length to 191 cos mysql versions can't handle unique values that have a 
    # character length that is greater than 191
    email = models.CharField( 
        null = False,
        unique = True,
        max_length = 191,
        blank = False,
        validators = [ validate_email, validate_unique_email ] 
    )
    
    password = models.CharField( 
        max_length = 255,
        blank = False,
        null = False
    )

    first_name = models.CharField( 
        max_length = 50,
        blank = False,
        null = False
    )
    
    last_name = models.CharField(
        max_length = 50,
        blank = False,
        null = False
    )

    is_active = models.BooleanField( 
        null = False,
        default = False
    )
    
    is_admin = models.BooleanField(
        null = False,
        default = True 
    )

    date_of_birth = models.DateField()
    
    phone = models.CharField(
        max_length = 11,
        blank = True
    )
    
    image = models.ImageField( 
        upload_to = 'media/users/', 
        blank = True
    )
    
    gender = models.CharField( 
        choices = GENDER, 
        default = MALE, 
        max_length = 50 
    )
    
    user_type = models.CharField( 
        choices = USER_TYPE, 
        default = TENANT, 
        max_length = 50 
    )
    
    bio_data = models.CharField( 
        max_length = 255, 
        null = True 
    )
    
    date_joined = models.DateTimeField( 
        auto_now_add = True, 
        editable = False 
    )
    
    last_login = models.DateTimeField( 
        auto_now = True, 
        editable = True 
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name', 'last_name', 'password',  ]
    
    def has_perm ( self, perm, obj = None ):
        return True
    
    def has_module_perms ( self, app_label ):
        return True
    
    @property
    def is_staff ( self ):
        return self.is_admin
    
    def get_fullname ( self ):
        return '{first_name} {last_name}'.format( 
            first_name = self.first_name, 
            last_name = self.last_name 
        )
    
    def get_short_name ( self ):
        return self.first_name
    
    def __str__ ( self ):
        self.get_fullname()
        
    def get_absolute_url ( self ):
        return reverse( 'auth_app:user_details', kwargs = { 'pk' : self.id } )
    

       
class ContactAddress ( models.Model ):
    user = models.OneToOneField( to = 'User', on_delete = models.CASCADE )
    address_line_1 = models.CharField( null = True, max_length = 255, blank = True )
    address_line_2 = models.CharField( null = True, max_length = 255, blank = True )
    location = models.ForeignKey( to = Location, on_delete = models.CASCADE )
    date_created = models.DateTimeField( auto_now_add = True, editable = False )
    date_updated = models.DateTimeField( auto_now = True, editable = True )

    class Meta:
        db_table = "contact_address_tbl"
        
        

class AdminUser ( models.Model ):
    user = models.OneToOneField( to = 'User', on_delete = models.CASCADE )
    date_created = models.DateTimeField( auto_now_add = True, editable = False )

    class Meta:
        db_table = "admin_tbl"
