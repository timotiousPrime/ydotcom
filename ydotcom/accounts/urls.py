from django.urls import path, include
from .views import loginPage, logoutPage, registerPage, UserProfileViewSet, UsersViewSet, InterestViewSet, EmploymentHistoryViewSet, newAccountApiView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user', UsersViewSet)
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'interest', InterestViewSet)
router.register(r'employment', EmploymentHistoryViewSet)

urlpatterns = [
    path("login/", loginPage.as_view(), name="Login"),
    path("logout/", logoutPage.as_view(), name="Logout"),
    path("register/", registerPage.as_view(), name="Register"),
    path("test/", views.testView, name="TestView"),
    path("user_account/", newAccountApiView.as_view(), name="newAccount"),
    path('api/', include (router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]