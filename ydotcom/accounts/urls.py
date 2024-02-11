from django.urls import path
from .views import accountsPage


urlpatterns = [
    path("", accountsPage.as_view(), name="accountsPage"),
]