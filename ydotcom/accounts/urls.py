from django.urls import path
from .views import loginPage, logoutPage, registerPage


urlpatterns = [
    path("login/", loginPage.as_view(), name="Login"),
    path("logout/", logoutPage.as_view(), name="Logout"),
    path("register/", registerPage.as_view(), name="Register"),
]