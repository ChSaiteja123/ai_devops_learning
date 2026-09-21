"""
Accounts URL patterns (API).

WHAT ARE URL PATTERNS?
-----------------------
URL patterns map URL strings to view functions or classes.
Each url() call is like a routing rule.

REST API conventions:
  GET    /resource/        → List all
  POST   /resource/        → Create new
  GET    /resource/{id}/   → Retrieve one
  PUT    /resource/{id}/   → Full update
  PATCH  /resource/{id}/   → Partial update
  DELETE /resource/{id}/   → Delete
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    path('users/<str:username>/', views.UserPublicProfileView.as_view(), name='user_public_profile'),
]
