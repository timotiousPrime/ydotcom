from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import landingPage, homePage


urlpatterns = [
    path("", landingPage.as_view(), name="LandingPage"),
    path("home/", login_required(homePage.as_view()), name="HomePage"),
]