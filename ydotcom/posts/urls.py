from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import User_Posts
# from . import views

urlpatterns = [
    path("<str:username>/", login_required(User_Posts.as_view()), name="User_Posts"),
]