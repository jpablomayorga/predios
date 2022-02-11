# django
from django.urls import include, path

# properties
from properties.api.views import (
    OwnerViewSet,
    EstateViewSet)

# rest_framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'owners', OwnerViewSet, basename='owners')
router.register(r'estates', EstateViewSet, basename='estates')

urlpatterns = [
    path('', include(router.urls)),
]
