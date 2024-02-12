from django.urls import path
from .views import accountsPage, loginPage, logoutPage, registerPage


urlpatterns = [
    path("", accountsPage.as_view(), name="Accounts_Page"),
    path("login/", loginPage.as_view(), name="Login"),
    path("logout/", logoutPage.as_view(), name="Logout"),
    path("register/", registerPage.as_view(), name="Register"),
]