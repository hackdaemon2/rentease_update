"""rentease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from auth_app import views
from main_app import views as main_views

app_name = 'auth_app'
urlpatterns = [
    path('login', views.AuthLoginView.as_view(), name = 'login'),
    path('logout', views.AuthLogoutView.as_view(), name = 'logout'),
    path('signup', views.AuthUserCreateView.as_view(), name = 'signup'),
    path('signup_success', views.AuthSignupSuccessView.as_view(), name = 'signup_success'),
    path('password_reset', views.AuthPasswordResetView.as_view(), name = 'password_reset'),
    path('password_reset/done', views.AuthPasswordResetDoneView.as_view(), name = 'password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.AuthPasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('reset/done', views.AuthPasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path('password_change', views.AuthPasswordChangeView.as_view(), name = 'password_change'),
    path('password_change/done', views.AuthPasswordChangeDoneView.as_view(), name = 'password_change_done'),
    path('settings', login_required ( views.SocialSettingsView.as_view() ), name='settings'),
    path('settings/password', login_required ( views.PasswordView.as_view() ), name='password'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.ActivateAccountView.as_view(), name='activate')
]
