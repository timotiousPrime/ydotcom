from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Post
from django.contrib.auth.models import User
from .forms import PostForm

from collections import defaultdict 


# Create your views here.
class User_Posts(View):
    template_name= "posts/userPosts.html"

    def get(self, request, username):
        # Get users and users posts and order by date
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user).order_by('-timestamp').values()
        
        # group posts per day 
        qs = defaultdict(list)
        for query in posts:
            post_date = query['timestamp'].date
            qs[post_date] += [query['message']]
        qs = dict(qs)

        context = {"title": f"{ username }'s Posts",
                   "posts": qs,
                   "poster": user}
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("User_Posts", request.user)
        return render(request, self.template_name, {"form": PostForm()})