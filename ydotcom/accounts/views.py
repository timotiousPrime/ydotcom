# Transactions
from django.db import transaction
# Views
from django.views.generic.edit import UpdateView
from django.views.generic import View
from django.contrib.auth.views import LoginView
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin
# Permissions
from django.core.exceptions import PermissionDenied

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
# Authentication
from django.contrib.auth import authenticate, login, logout
# Models
from django.contrib.auth.models import User
from .models import UserProfile, Interest, EmploymentHistory
# Forms
from .forms import UserRegisterForm, UserProfileForm, EmploymentHistoryFormSet
from django.contrib.auth.forms import AuthenticationForm
# DRF
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
# serializers
from .serializers import UserProfileSerializer, InterestSerializer, EmploymentHistorySerializer
# Messages
from django.contrib import messages
# Email 
# from django.template.loader import get_template
# from django.core.mail import EmailMultiAlternatives



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
    
    @transaction.atomic
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
    

###############################################
#####           API Views                 #####
###############################################
    
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EmploymentHistoryViewSet(viewsets.ModelViewSet):
    queryset = EmploymentHistory.objects.all()
    serializer_class = EmploymentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_profile_id = self.kwargs.get('user_profile_id')
        if user_profile_id:
            return self.queryset.filter(user_profile_id=user_profile_id)
        return self.queryset


###############################################
#####           End API Views             #####
###############################################
    
# Front end views
    

class userManagerView(View):
    template_name = "accounts/accountsManager.html"
    title = "Account Manager "
    registerForm = UserRegisterForm

    def get(self, request):
        context = {"title": self.title,
                   "form": self.registerForm}
        return render(request, self.template_name, context)
    

    
class UserProfileViewSet(viewsets.ModelViewSet):
    @transaction.atomic
    def create_full_profile(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile_update.html'

    def get_object(self, queryset=None):
        obj = super(UserProfileUpdateView, self).get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this profile.")
        return obj

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UserRegisterForm(self.request.POST, instance=self.request.user)
            context['employmenthistory_form'] = EmploymentHistoryFormSet(self.request.POST, instance=self.object)
        else:
            context['user_form'] = UserRegisterForm(instance=self.request.user)
            context['employmenthistory_form'] = EmploymentHistoryFormSet(instance=self.object)
        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        employmenthistory_form = context['employmenthistory_form']
        if user_form.is_valid() and employmenthistory_form.is_valid():
            self.object = form.save()
            user_form.save()
            employmenthistory_form.instance = self.object
            employmenthistory_form.save()
            return super(UserProfileUpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
    def get_success_url(self):
        return redirect('profile-detail', kwargs={'pk': self.object.pk})
        # Make url for profile detail!!!
    
