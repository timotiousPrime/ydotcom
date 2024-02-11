from django.urls import path
from .views import accountsPage, loginPage, logoutPage, registerPage


urlpatterns = [
    path("", accountsPage.as_view(), name="accountsPage"),
    path("login/", loginPage.as_view(), name="login"),
    path("logout/", logoutPage.as_view(), name="logout"),
    path("register/", registerPage.as_view(), name="register"),
]