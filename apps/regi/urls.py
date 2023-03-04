from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PatientView, RegiStaffView
)

app_name = 'apps.account'

router = DefaultRouter()
router.register('patient', PatientView, basename='patient',)
router.register('registaff', RegiStaffView, basename='registaff',)

urlpatterns = router.urls

# urlpatterns = [
#     path('register/', CreateAccount.as_view(), name="create_account"),
# ]