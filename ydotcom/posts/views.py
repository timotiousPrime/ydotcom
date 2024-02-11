from django.shortcuts import render
from django.views.generic import View


# Create your views here.
class postsPage(View):
    template_name = "posts/postsPage.html"
    title = "Hello, World. Welcome to the posts page"

    def get(self, request):
        context = {"title": self.title}
        return render(request, self.template_name, context)