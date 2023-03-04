from rest_framework import serializers
from apps.regi.models import (Patient, RegiStaff)


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ('__all__')
        # fields = ('first_name', 'last_name', 'address', 'sex', 'phone', 'dob',)
    

class RegiStaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegiStaff
        fields = ('__all__')
        # fields = ('first_name', 'last_name', 'address', 'sex', 'phone', 'dob',)
