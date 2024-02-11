# from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render


# Create your views here.
class landingPage(View):
    template_name = "main/landingPage.html"
    title = "Hello, World. Welcome to the landing Page"

    def get(self, request):
        context = {"title": self.title}
        return render(request, self.template_name, context)