from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('documents', views.DocumentViewSet, basename='rag-document')

urlpatterns = [
    path('', include(router.urls)),
    path('query/', views.query_knowledge_base, name='rag_query'),
    path('history/', views.query_history, name='rag_history'),
]
