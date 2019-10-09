"""Url config for django rest framework"""
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as auth_views
from backend import views

# router = routers.DefaultRouter()

urlpatterns = [
    # path('', include(router.urls)),
    path(r'jwt-auth/', views.auth_views.CustomAuthToken.as_view(), name='account-auth'),
    path(r'jwt-auth2/', auth_views.obtain_auth_token),
    # path(r'api/auth/', include('rest_framework.urls')),
    path(r'api/signup/', views.StudentList.as_view()),
    path(r'accounts/students/', views.StudentList.as_view(), name='student-list'),
    path(r'accounts/students/<int:pk>/', views.StudentDetail.as_view(), name='student-detail'),
]
