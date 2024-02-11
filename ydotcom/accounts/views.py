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