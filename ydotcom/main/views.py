# from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.models import User
from posts.models import Post



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

    def get(self, request):
        posts = Post.objects.all().order_by('-timestamp')
        context = {"title": self.title,
                   "posts": posts,
                   }
        return render(request, self.template_name, context)