from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UPatientView, XPatientView, UExamView, XExamView, UExamItemView, 
    XExamItemView, UFindingView, XFindingView, RadiDeptView, RadiStaffView,
    RadiTestCategoryView, RadiTestTypeView
)

app_name = 'apps.account'

router = DefaultRouter()
router.register('upatient', UPatientView, basename='upatient',)
router.register('xpatient', XPatientView, basename='xpatient',)
router.register('uexam', UExamView, basename='uexam',)
router.register('xexam', XExamView, basename='xexam',)
router.register('uexamitem', UExamItemView, basename='uexamitem',)
router.register('xexamitem', XExamItemView, basename='xexamitem',)
router.register('ufinding', UFindingView, basename='ufinding',)
router.register('xfinding', XFindingView, basename='xfinding',)
router.register('radidept', RadiDeptView, basename='radidept',)
router.register('radistaff', RadiStaffView, basename='radistaff',)
router.register('raditestcategory', RadiTestCategoryView, basename='raditestcategory',)
router.register('raditesttype', RadiTestTypeView, basename='raditesttype',)

urlpatterns = router.urls

# urlpatterns = [
#     path('register/', CreateAccount.as_view(), name="create_account"),
# ]