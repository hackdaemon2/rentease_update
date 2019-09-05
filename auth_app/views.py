from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView 
from django.views import View
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponseRedirect

from auth_app.forms import AuthSetPasswordForm
from auth_app.forms import AuthForm as AuthenticationForm
from auth_app.forms import AuthPasswordChangeForm
from auth_app.forms import AuthUserCreationForm
from auth_app.forms import AuthPasswordResetForm
from auth_app.tokens import account_activation_token
from auth_app.models import User

from social_django.models import UserSocialAuth



# Create your views here

context = { 
    'current_year' : timezone.now().year,
    'app_name' : settings.APP_NAME,
}


class SocialSettingsView ( TemplateView ):
    template_name = 'auth_app/settings.html'
    extra_context = context
    
    def get ( self, *args, **kwargs  ):
        user = self.request.user

        try:
            google_login = user.social_auth.get(provider='google')
        except UserSocialAuth.DoesNotExist:
            google_login = None

        try:
            facebook_login = user.social_auth.get(provider='facebook')
        except UserSocialAuth.DoesNotExist:
            facebook_login = None

        can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
        
        settings_context = {
            'google_login': google_login,
            'facebook_login': facebook_login,
            'can_disconnect': can_disconnect
        }
        
        self.extra_context.extend( settings_context )
        
        return super( SocialSettingsView ).get( *args, **kwargs )




class PasswordView ( TemplateView ):
    template_name = 'auth_app/password.html'
    redirect_url = reverse_lazy ( 'auth_app:password' )
    form_class = PasswordChangeForm
    extra_context = context
    
    def form_valid ( self, form ):
        form.save()
        update_session_auth_hash( self.request, form.user )
            
        form_is_valid = super().form_valid( form )
        
        if form_is_valid:
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect( redirect_url )
        else:
            messages.error(request, 'Please correct the error below.')
            
        return form_is_valid



class AuthLoginView ( auth_views.LoginView ):
    template_name = 'auth_app/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    extra_context = context



class AuthLogoutView ( auth_views.LogoutView ):
    next_page = reverse_lazy ( 'auth:login' )   



class AuthPasswordChangeView ( auth_views.PasswordChangeView ):
    template_name = 'auth_app/password_change.html'
    success_url = reverse_lazy ( 'auth_app:password_change_done' )
    form_class = AuthPasswordChangeForm
    extra_context = context
      

    
class AuthPasswordChangeDoneView ( auth_views.PasswordChangeView ):
    template_name = 'auth_app/password_change_done.html'
    extra_context = context
    
    

class AuthPasswordResetDoneView ( auth_views.PasswordResetDoneView ):
    template_name = 'auth_app/password_reset_done.html'
    extra_context = context
    


class AuthPasswordResetView ( auth_views.PasswordResetView ):
    template_name = 'auth_app/password_reset.html'   
    # generates the email message with the password reset link
    form_class = AuthPasswordResetForm
    email_template_name = 'auth_app/password_reset_email.html' 
    subject_template_name = 'auth_app/password_reset_subject.txt'
    success_url = reverse_lazy ( 'auth_app:password_reset_done' )
    from_email = settings.DEFAULT_FROM_EMAIL
    html_email_template_name = 'auth_app/password_reset_email.html'
    extra_context = context
    
    
    
class AuthPasswordResetConfirmView ( auth_views.PasswordResetConfirmView ):
    template_name = 'auth_app/password_reset_confirm.html'
    form_class = AuthSetPasswordForm
    success_url = reverse_lazy ( 'auth_app:password_reset_complete' )  
    extra_context = context
    
      
    
class AuthPasswordResetCompleteView ( TemplateView ):
    template_name = 'auth_app/password_reset_complete.html'
    extra_context = context
    
    

class AuthUserCreateView ( CreateView ):
    template_name = 'auth_app/signup.html'
    model = settings.AUTH_USER_MODEL
    form_class = AuthUserCreationForm
    success_url = reverse_lazy('auth_app:signup_success')
    extra_context = context
    
    def form_valid ( self, form ):
        user = form.save( commit = False )
        user.is_active = False
        
        user.save()
        
        current_site = get_current_site ( self.request )
        mail_subject = 'Activate your Rentease Account'
        
        mail_context = {
            'user' : user,
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : account_activation_token.make_token(user),
        }
        
        message = render_to_string ( 'auth_app/account_activate_email.html', mail_context )
        to_email = form.cleaned_data['email']
        
        email = EmailMessage( mail_subject, message, to = [ to_email ] )
        email.content_subtype = 'html'
        email.send()
        
        return super().form_valid(form)
    
    
    
class ActivateAccountView ( TemplateView ):
    template_name = 'auth_app/activate.html'
    
    def get_context_data ( self, **kwargs ):
        context = super().get_context_data( **kwargs )
        
        uidb64 = kwargs.pop('uidb64')
        token = kwargs.pop('token')
        
        try:
            uid = force_text ( urlsafe_base64_decode( uidb64 ).decode() )
            user = User.objects.get( pk = uid )
        except ( ValueError, TypeError, OverflowError, User.DoesNotExist ):
            user = None
        
        if user is not None and account_activation_token.check_token( user, token ):
            user.is_active = True
            user.save()
            context['activation_status'] = True
            context['user_email'] = user.email
        else:
            context['activation_status'] = False
            
        context['support_email'] = settings.SUPPORT_EMAIL
        context['app_name'] = settings.APP_NAME
        
        return context



class AuthSignupSuccessView ( TemplateView ):
    template_name = 'auth_app/signup_success.html'
    extra_context = context
    
    
    

    


