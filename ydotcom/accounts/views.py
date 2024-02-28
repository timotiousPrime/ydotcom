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
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, InterestSerializer, EmploymentHistorySerializer, UserAccountSerializer, UserSerializer
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
    
    @transaction.atomic
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

class UsersList(APIView):
    def get(self, request):
        queryset = User.objects.all()
        return Response ({'queryset': queryset})
    

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

###############################################
#####           End API Views             #####
###############################################
    
# Front end views
    
def testView(request):
    template = "accounts/test.html"
    context = {
        "title": "Test Page"
    }
    return render(request, template, context)

class newAccountApiView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()

    def get(self, request):
        user = User.objects.all()

        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, format=None):
        data = request.data
        # Extract user data and create user
        user_data = data.get('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract Profile data and create userProfile instance, associated with newly created user
        profile_data = data.get('profile')
        profile_serializer = UserProfileSerializer(data=profile_data, context={'user': user.pk})
        if profile_serializer.is_valid():
            profile = profile_serializer.save(user=user)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract employment history data and create EmploymentHistory instances
        employment_data = profile_data.get('employement', [])
        for employment_item in employment_data:
            employment_serializer = EmploymentHistorySerializer(data=employment_item, context={'user_profile': profile.pk})
            if employment_serializer.is_valid():
                employment_serializer.save(profile=profile)
            else:
                return Response(employment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data,
            'employment_history': [EmploymentHistorySerializer(employment).data for employment in profile.employmenthistory_set.all()],

        }, status=status.HTTP_201_CREATED)
