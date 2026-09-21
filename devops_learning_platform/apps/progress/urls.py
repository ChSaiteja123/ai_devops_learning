from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('enrollments', views.EnrollmentViewSet, basename='enrollment')
router.register('certificates', views.CertificateViewSet, basename='certificate')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.learning_dashboard, name='learning_dashboard'),
]
