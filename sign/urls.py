from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from .views import upgrade_me

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='accounts/signup.html'), name='signup'),
    path('upgrade/', upgrade_me, name='upgrade')
]