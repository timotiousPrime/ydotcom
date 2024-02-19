from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from collections import defaultdict 


# Create your views here.

@login_required
def userPostsList(request, username):
    if request.method == "GET":
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user = user.id).order_by('-timestamp')
        form = PostForm()

        # group posts per day 
        qs = defaultdict(list)
        for query in posts:
            post_date = query.timestamp.date
            qs[post_date] += [query.message]
        qs = dict(qs)

        context = {
            "title": username,  
            "posts": qs,
            "poster": User.objects.get(username=username),
            "form": form
        }
        return render(request, "posts/userPosts.html", context)

@login_required
def createPost(request, username):
    user = get_object_or_404(User, username=request.user.username)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
            return redirect("User_Posts", user.username)
    else:
        form = PostForm()

    context = {
        "form": form,
        "user": user
    }
    print(context['form'])
    return render(request, "posts/userPosts.html", context)
