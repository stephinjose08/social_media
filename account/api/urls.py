from rest_framework_simplejwt.views import (
  
    TokenRefreshView,TokenObtainPairView
)
from rest_framework.routers import DefaultRouter
from .views import UserCreateView,MyTokenObtainPairView
from django.contrib import admin
from django.urls import include, path
from .views import profile_Viewset
router = DefaultRouter()
router.register('profile', profile_Viewset, basename='profile')
urlpatterns = [
    path('',include(router.urls)),

    path('login/', MyTokenObtainPairView.as_view(), name='login-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateView.as_view(),name='user-create'),
]
