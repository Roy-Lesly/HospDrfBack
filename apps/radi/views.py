from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import (
        UPatientSerializer, XPatientSerializer, UExamSerializer, XExamSerializer,
        UExamItemSerializer, XExamItemSerializer, RadiDeptSerializer, 
        RadiStaffSerializer, RadiTestCategorySerializer, RadiTestTypeSerializer,
        UFindingSerializer, XFindingSerializer,
    )
from .models import (
        UPatient, XPatient, UExam, XExam, UExamItem, XExamItem,
        UFinding, XFinding, RadiDept, RadiStaff, RadiTestCategory, 
        RadiTestType,
    )


class UPatientView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UPatientSerializer
    queryset = UPatient.objects.all()

class XPatientView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = XPatientSerializer
    queryset = XPatient.objects.all()

class UExamView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UExamSerializer
    queryset = UExam.objects.all()

class XExamView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = XExamSerializer
    queryset = XExam.objects.all()

class UExamItemView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UExamItemSerializer
    queryset = UExamItem.objects.all()

class XExamItemView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = XExamItemSerializer
    queryset = XExamItem.objects.all()

class UFindingView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UFindingSerializer
    queryset = UFinding.objects.all()

class XFindingView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = XFindingSerializer
    queryset = XFinding.objects.all()

class RadiDeptView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = RadiDeptSerializer
    queryset = RadiDept.objects.all()

class RadiStaffView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = RadiStaffSerializer
    queryset = RadiStaff.objects.all()

class RadiTestCategoryView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = RadiTestCategorySerializer
    queryset = RadiTestCategory.objects.all()

class RadiTestTypeView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = RadiTestTypeSerializer
    queryset = RadiTestType.objects.all()
