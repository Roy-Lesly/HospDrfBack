from rest_framework import serializers
from apps.radi.models import (
        UPatient, XPatient, UExam, XExam, UExamItem, XExamItem,
        UFinding, XFinding,
        RadiStaff, RadiDept, RadiTestCategory, RadiTestType, RadiHanding
    )


class UPatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = UPatient
        fields = ('__all__')

class XPatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = XPatient
        fields = ('__all__')
    
class UExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = UExam
        fields = ('__all__')

class XExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = XExam
        fields = ('__all__')

class UExamItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UExamItem
        fields = ('__all__')

class XExamItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = XExamItem
        fields = ('__all__')

class UFindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UFinding
        fields = ('__all__')

class XFindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = XFinding
        fields = ('__all__')

class RadiDeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiDept
        fields = ('__all__')

class RadiStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiStaff
        fields = ('__all__')

class RadiTestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiTestCategory
        fields = ('__all__')

class RadiTestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiTestType
        fields = ('__all__')