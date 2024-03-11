from django.urls import path, include
from .views import (loginPage, 
                    logoutPage, 
                    registerPage, 
                    UserProfileViewSet, 
                    UsersViewSet, 
                    InterestViewSet, 
                    EmploymentHistoryViewSet, 
                    EmploymentHistoryDeleteView,
                    newAccountApiView, 
                    AccountsListView,
                    AccountDetailView,
                    AccountDeleteView,
                    ProfileUpdateView,
                    NewAccount,
                    )
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user', UsersViewSet)
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'interest', InterestViewSet)
router.register(r'employment', EmploymentHistoryViewSet)

app_name = "accounts"

urlpatterns = [
    path("login/", loginPage.as_view(), name="Login"),
    path("logout/", logoutPage.as_view(), name="Logout"),
    path("register/", registerPage.as_view(), name="Register"),
    
    path("", AccountsListView.as_view(), name="Accounts"),
    path("new/", NewAccount.as_view(), name="NewAccount"),
    # path("update/<int:pk>", AccountUpdate.as_view(), name="AccountUpdate"),
    path("delete/<int:pk>", AccountDeleteView.as_view(), name="AccountDelete"),
    path("employment/delete/<int:pk>", EmploymentHistoryDeleteView.as_view(), name="EmploymentHistoryDelete"),
    path("<int:pk>", AccountDetailView.as_view(), name="AccountDetails"),
    path("profile/<int:pk>", ProfileUpdateView.as_view(), name="ProfileUpdate"),

    # path("", AccountsPage.as_view(), name="Accounts"),
    # path("<str:username>", UserDetails.as_view(), name="UserDetails"),
    # path("test/", views.testView, name="TestView"),
    # path("user_account/", newAccountApiView.as_view(), name="newAccount"),

    path('api/', include (router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]