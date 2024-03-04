# Transactions
from django.db import transaction
# Views
from django.views.generic.edit import UpdateView
from django.views.generic import View, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.views import LoginView
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin
# Permissions
from django.core.exceptions import PermissionDenied

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
# Authentication
from django.contrib.auth import authenticate, login, logout
# Models
from django.contrib.auth.models import User
from .models import UserProfile, Interest, EmploymentHistory
# Forms
from .forms import UserRegisterForm, UserProfileForm, UserformSet, UserAccountForm, EmploymentHistoryFormSet
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
# class accountsPage(View):
#     template_name = "accounts/accountsPage.html"
#     title = "Hello, World. Welcome to the accounts Page"

#     def get(self, request):
#         context = {"title": self.title}
#         return render(request, self.template_name, context)
    
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
    
# AccountsListView
class AccountsListView(ListView):
    template_name = "accounts/accountsListPage.html"
    queryset = User.objects.all()

# AccountDetailView
class AccountDetailView(DetailView):
    template_name = "accounts/accountDetailPage.html"
    model = User

# AccountCreateView
class NewAccount(View):
    template_name = "accounts/accountsCreatePage.html"

    def get(self, request, *args, **kwargs):
        user_form = UserAccountForm()
        profile_form = UserProfileForm()
        history_formset = EmploymentHistoryFormSet()
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'history_formset': history_formset,
        })

    def post(self, request, *args, **kwargs):
        user_form = UserAccountForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        history_formset = EmploymentHistoryFormSet(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save() # creates new user, which sends signal to create new profile
                print("userSaved!")
                profile_form.instance.user = user
                profile_form.save()
                history_formset = EmploymentHistoryFormSet(request.POST, instance=user)
                if history_formset.is_valid():
                    history_formset.save()
                    messages.success(request, "User and associated profile created successfully.")
                    return HttpResponseRedirect(reverse('accounts:Accounts'))

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'history_formset': history_formset,
        })

# AccountDeleteView
    
# UserProfileDetailView
# UserProfileUpdateView
class ProfileUpdateView(SingleObjectMixin, FormView):
    model = UserProfile
    template_name = "accounts/profileEdit.html"
    # fields = ['first_name', 'surname', 'title', 'email', 'phone_number', 'date_of_birth', 'interests']
    form_class = UserProfileForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("posting....")
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form_class = self.get_form_class() if form_class is None else form_class
        return UserformSet(**self.get_form_kwargs(), instance=self.object.user)
    
    def form_valid(self, form):
        with transaction.atomic():
            form.save()
            print("Profile Update saved successfully!")
            messages.add_message(self.request, messages.SUCCESS, "Changes were saved!")
            return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('accounts:AccountDetails', kwargs={"pk": self.object.user.pk})
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
# UserEmploymentHistoryListView
# UserEmploymentHistoryDetailView
# UserEmploymentHistoryUpdateView
# UserEmploymentHistoryDeleteView
    
# def testView(request):
#     template = "accounts/test.html"
#     context = {
#         "title": "Test Page"
#     }
#     return render(request, template, context)

# class AccountsPage(ListView):
#     template_name = "accounts/accountsPage.html"
#     form_class = UserAccountForm
#     queryset = User.objects.all()

# class UserDetails(DetailView):
#     model = User
#     template_name = "accounts/userDetailsPage.html"

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
