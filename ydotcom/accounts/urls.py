from django.urls import path, include
from .views import loginPage, logoutPage, registerPage, UserProfileViewSet, InterestViewSet, EmploymentHistoryViewSet, UserProfileUpdateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='user')
router.register(r'interest', InterestViewSet)
router.register(r'employment', EmploymentHistoryViewSet)

urlpatterns = [
    path("login/", loginPage.as_view(), name="Login"),
    path("logout/", logoutPage.as_view(), name="Logout"),
    path("register/", registerPage.as_view(), name="Register"),
    path("profile/edit/<str:username>", UserProfileUpdateView.as_view(), name="Edit_Profile"),

    path('api/', include (router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]