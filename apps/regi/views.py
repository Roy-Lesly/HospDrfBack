from rest_framework import status
import datetime
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .serializers import (
        PatientSerializer, RegiStaffSerializer
    )
from .models import Patient, RegiStaff


class PatientView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    def create(self, request: Request):
        data = request.data
        _mutable = data._mutable
        data._mutable = True
        print("CREATE PATIENT VIEW ==>  ", data)
        now = datetime.date.today()
        if len(str(data['reg_num'])) < 5:
            reg_num = str(data['reg_num']).zfill(5) + "-" + str(now.year)[2:4]
        if len(str(data['reg_num'])) == 5:
            reg_num = str(data['reg_num']) + "-" + str(now.year)[2:4]
        data['reg_num'] = reg_num
        print("HERE")
        dob = datetime.date.today()
        print(dob)
        data["dob"] = dob  
        print("CREATE PATIENT VIEW2 ==>  ", data)
        data._mutable = _mutable

        print(data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Patient Created Successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, pk=None, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        num = data["reg_num"]
        now = datetime.date.today()
        if len(str(num)) < 5:
            reg_num = str(num).zfill(6) + "_" + str(now.year)[2:4]
        if len(str(now)) == 6:
            reg_num = str(num) + "_" + str(now.year)[2:4]
        data["reg_num"] = reg_num
        # print(data)
        serializer = self.get_serializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, pk=None, *args, **kwargs):
        print("DELETE")
        try:
            # return super().destroy(request, *args, **kwargs)
            super().destroy(request, *args, **kwargs)
            return Response(data="Patient Deleted Successfully", status=status.HTTP_200_OK)

        except:
            return Response(data="Patient Do Not Exist", status=status.HTTP_404_NOT_FOUND)

class RegiStaffView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = RegiStaffSerializer
    queryset = RegiStaff.objects.all()


