from rest_framework_simplejwt.views import (
  
    TokenRefreshView,TokenObtainPairView
)
from rest_framework.routers import DefaultRouter
from .views import UserCreateView,MyTokenObtainPairView,UserListView
from django.contrib import admin
from django.urls import include, path
from .views import profile_Viewset,followOrUnfollowViewset
router = DefaultRouter()
router.register('profile', profile_Viewset, basename='profile')
urlpatterns = [
    path('',include(router.urls)),

    path('login/', MyTokenObtainPairView.as_view(), name='login-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateView.as_view(),name='user-create'),
    path('list/', UserListView.as_view(),name='user-list'),

    path('is_follow/<int:pk>/', followOrUnfollowViewset.as_view(),name='user-list'),

]
