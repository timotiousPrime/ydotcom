from django.urls import path
from .views import postsPage
# from . import views

urlpatterns = [
    path("posts", postsPage.as_view(), name="posts"),
]