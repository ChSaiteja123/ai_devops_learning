"""HTML page URLs for authentication (login/register forms)."""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True), name='login'),
    path('register/', TemplateView.as_view(template_name='accounts/register.html'), name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', TemplateView.as_view(template_name='accounts/profile.html'), name='profile_page'),
]
