from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
# Authentication
from django.contrib.auth import authenticate, login, logout
# Models
from django.contrib.auth.models import User
# Forms
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
# Messages
from django.contrib import messages
# Email 
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives



# Create your views here.
class accountsPage(View):
    template_name = "accounts/accountsPage.html"
    title = "Hello, World. Welcome to the accounts Page"

    def get(self, request):
        context = {"title": self.title}
        return render(request, self.template_name, context)
    
# This will change to a redirect
class loginPage(LoginView):
    template_name = "accounts/login.html"
    title = "Login Page"
    loginForm = AuthenticationForm()
    redirect_authenticated_user = True
    next_page = "/home"
    
    def get(self, request):
        context = {"title": self.title,
                   "form": self.loginForm}
        return render(request, self.template_name, context)
    
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f"Welcome back {username}!")
            return redirect('HomePage')
        else:
            messages.info(request, f"That account doesn't seem to exist. Please try login again.")
            context = {
                "title": self.title,
                "form": self.loginForm
            }
            return render(request, self.template_name, context)
    
    
class logoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('LandingPage')
    
    
class registerPage(View):
    template_name = "accounts/register.html"
    title = "Register Page"
    registerForm = UserRegisterForm

    def get(self, request):
        context = {"title": self.title,
                   "form": self.registerForm}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.registerForm(request.POST)
        context = {
            "title": self.title,
            "form": form
        }
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            ''' 
            IF YOU WANT EMAIL CONFIRMATION 
            '''
            # Email authentication
            # htmly = get_template('main/Email.html')
            # d = {'username': username}
            # subject, from_email, to = 'welcome', 'timodb031@gmail.com', email
            # html_content = htmly.render(d)
            # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            # Success
            messages.success(request, f"Congratulations! Your account has been created! You can now log in.")
            return redirect('Login') 
        return render(request, self.template_name, context)