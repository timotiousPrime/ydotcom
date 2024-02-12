# from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.models import User



# Create your views here.

# redirect to login page or user home
class landingPage(View):
    template_name = "main/landingPage.html"
    title = "Hello, World. Welcome to the landing Page"

    def get(self, request):
        context = {"title": self.title}
        return render(request, self.template_name, context)
    

class homePage(View):
    template_name = "main/homePage.html"
    title = "Home Page"
    users = User.objects.all()

    def get(self, request):
        context = {"title": self.title,
                   "users": self.users,
                   }
        return render(request, self.template_name, context)