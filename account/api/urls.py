from rest_framework_simplejwt.views import (
  
    TokenRefreshView,TokenObtainPairView
)
from rest_framework.routers import DefaultRouter
from .views import UserCreateView,MyTokenObtainPairView,UserListView
from django.contrib import admin
from django.urls import include, path
from .views import profile_Viewset,followOrUnfollowViewset,block_user,logout_view
router = DefaultRouter()
router.register('profile', profile_Viewset, basename='profile')
urlpatterns = [
    path('',include(router.urls)),

    path('login/', MyTokenObtainPairView.as_view(), name='login-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateView.as_view(),name='user-create'),
    path('logout/', logout_view.as_view(),name='log-out'),
    path('list/', UserListView.as_view(),name='user-list'),

    path('is_follow/<int:pk>/', followOrUnfollowViewset.as_view(),name='user-list'),
    path('block/<int:pk>/', block_user.as_view(),name='block-user'),

]
