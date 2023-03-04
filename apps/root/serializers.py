from rest_framework import serializers
from apps.regi.models import (Ward, )


class WardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ward
        fields = ('__all__',)
