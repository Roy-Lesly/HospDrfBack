from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    WardView, 
)

app_name = 'apps.root'

router = DefaultRouter()
router.register('ward', WardView, basename='ward',)

urlpatterns = router.urls
