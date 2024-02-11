from django.urls import path
from .views import landingPage


urlpatterns = [
    path("", landingPage.as_view(), name="Home"),
]