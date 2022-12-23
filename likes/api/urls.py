from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import likeViewset


router = DefaultRouter()
router.register('', likeViewset, basename='likes')
urlpatterns = [
    path('',include(router.urls)),
]