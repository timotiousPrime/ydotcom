# from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render


# Create your views here.
class accountsPage(View):
    template_name = "accounts/accountsPage.html"
    title = "Hello, World. Welcome to the accounts Page"

    def get(self, request):
        context = {"title": self.title}
        return render(request, self.template_name, context)
    
    
class loginPage(View):
    template_name = "accounts/login.html"
    title = "Hello, World. Welcome to the login Page"

    def get(self, request):
        context = {"title": self.title}
        return render(request, self.template_name, context)
    
    
class logoutPage(View):
    template_name = "accounts/logout.html"
    title = "Hello, World. Welcome to the logout Page"

    def get(self, request):
        context = {"title": self.title}
        return render(request, self.template_name, context)
    
    
class registerPage(View):
    template_name = "accounts/register.html"
    title = "Hello, World. Welcome to the register Page"

    def get(self, request):
        context = {"title": self.title}
        return render(request, self.template_name, context)