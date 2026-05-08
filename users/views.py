from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import RegistrationForm, LoginForm

class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        user = self.request.user
        if user.role == 'seller':
            return reverse_lazy('seller_dashboard')
        return reverse_lazy('browse')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
