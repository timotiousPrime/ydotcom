from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("<str:username>/", login_required(views.userPostsList), name="User_Posts"),
    path("<str:username>/create", login_required(views.createPost), name="New_Post"),
]