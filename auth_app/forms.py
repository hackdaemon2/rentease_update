from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from auth_app.models import User
from django import forms
from django.utils import timezone



class AuthUserCreationForm ( forms.ModelForm ):
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Email',
                'min_length' : 5,
                'max_length' : 191,
                'autocomplete' : 'off',
                'id' : 'email',
            }
        ),
        required = True,
        label = '* Email',
    )
    
    user_type = forms.CharField(
        widget = forms.Select(
            choices = User.USER_TYPE,
            attrs = {
                'class' : 'form-control js-example-basic-single',
                'width' : '100%',
                'id' : 'type',
            }
        ),
        label = '* User Type',
    )
    
    gender = forms.CharField(
        widget = forms.Select(
            choices = User.GENDER,
            attrs = {
                'class' : 'form-control js-example-basic-single',
                'width' : '100%',
                'id' : 'gender',
            }
        ),
        label = '* Gender',
    )
    
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Password',
                'min_length' : 8,
                'max_length' : 255,
                'id' : 'password',
            }
        ),
        required = True,
        label = '* Password',
        help_text = 'Password must be made up of 8 alphanumeric characters',
    )
    
    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Confirm Password',
                'min_length' : 8,
                'max_length' : 255,
                'id' : 'confirm_password',
            }
        ), 
        help_text = 'Confirm password must match password',
        label = '* Confirm Password',
    )
    
    first_name = forms.CharField( 
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'First Name',
                'min_length' : 2,
                'max_length' : 50,
                'autocomplete' : 'off',
            }
        ),
        required = True,
        label = '* First Name'
    )
    
    last_name = forms.CharField( 
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Last Name',
                'min_length' : 2,
                'max_length' : 50,
                'autocomplete' : 'off',
            }
        ),
        required = True,
        label = '* Last Name',
    )
    
    def clean_password2 ( self ):
        # Check that the two password entries match
        password1 = self.cleaned_data.get( 'password' )
        password2 = self.cleaned_data.get( 'password2' )
    
        if password1 and password2 and ( password1 != password2 ):
            raise forms.ValidationError('Passwords don\'t match')
        
        return password2
    
    def clean_email ( self ):
        email = self.cleaned_data.get('email')    
        email_exists = User.objects.filter( email__exact = email )
        
        if email_exists:
            raise forms.ValidationError('This email already exists in our database')
        
        return email

    def save ( self, commit = True ):
        # Save the provided password in hashed format
        user = super().save( commit = False )
        user.set_password(self.cleaned_data['password'])
        user.date_of_birth = timezone.now()
        
        if commit:
            user.save()
        
        return user

    class Meta:
        model = User
        fields = ( 'email', 'user_type', 'first_name', 'last_name', 'password', 'gender' )    
    


class AuthUserChangeForm ( forms.ModelForm ):
    """ A form for changing the user data """
    
    password = ReadOnlyPasswordHashField()
    
    def clean_password ( self ):
        return self.initial["password"]
    
    def clean_phone ( self ):
        phone = self.cleaned_data.get('phone')    
        phone_exists = User.objects.filter( phone__exact = phone )
        
        if phone_exists:
            raise forms.ValidationError('This phone number already exists in our database')
        
    class Meta:
        model = User
        fields = ( 
            'first_name',
            'last_name',
            'phone',
            'image',
            'gender',
            'bio_data',
            'date_of_birth', 
            'is_active', 
            'is_admin',
        )


    
class AuthPasswordChangeForm ( auth_forms.PasswordChangeForm ):
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Password',
                'min_length' : 8,
                'max_length' : 255,
                'id':'new_password',
            }
        ),
        required = True,
        help_text = 'Password is required'
    )
    
    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Confirm Password',
                'min_length' : 8,
                'max_length' : 255,
                'id':'confirm_new_password',
            }
        ), 
        required = True,
        help_text = 'Confirm password must match password'
    )

    class Meta:
        model = User
        fields = ( 'password' )
    
    def clean_password2 ( self ):
        # Check that the two password entries match
        password1 = self.cleaned_data.get( 'password' )
        password2 = self.cleaned_data.get( 'password2' )
    
        if password1 and password2 and ( password1 != password2 ):
            raise forms.ValidationError('Passwords don\'t match')
        
        return password2

    def save ( self, commit = True ):
        # Save the provided password in hashed format
        user = super().save( commit = False )
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        
        return user


class AuthPasswordResetForm ( auth_forms.PasswordResetForm ):
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Email',
                'max_length' : 191,
                'min_length' : 5,
                'id' : 'email',
                'autocomplete' : 'off',
            }
        ),
        required = True
    )   



class AuthForm ( auth_forms.AuthenticationForm ):
    username = forms.CharField(
        label = "Email",
        widget = forms.EmailInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Email',
                'autofocus' : True,
                'autocomplete' : 'off',
                'min_length' : 5,
                'max_length' : 191,
            }
        ),
        required = True,
    )
    
    password = forms.CharField(
        label = "Password",
        widget = forms.PasswordInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Password',
                'min_length' : 8,
                'max_length' : 255,
            }
            
        ),
        required = True
    )
    


class AuthSetPasswordForm ( auth_forms.SetPasswordForm ):
    new_password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'New Password',
                'min_length' : 8,
                'max_length' : 255,
            }
        ),
        required = True,
        help_text = 'Password is required'
    )
    
    new_password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Confirm New Password',
                'min_length' : 8,
                'max_length' : 255,
            }
        ), 
        required = True,
        help_text = 'Confirm password must match password'
    )

    class Meta:
        model = User
        fields = ( 'password' )
    
    def clean_password2 ( self ):
        # Check that the two password entries match
        password1 = self.cleaned_data.get( 'new_password1' )
        password2 = self.cleaned_data.get( 'new_password2' )
    
        if password1 and password2 and ( password1 != password2 ):
            raise forms.ValidationError('Passwords don\'t match')
        
        return password2

    def save ( self, commit = True ):
        # Save the provided password in hashed format
        user = super().save( commit = False )
        user.set_password(self.cleaned_data['new_password1'])
        
        if commit:
            user.save()
        
        return user