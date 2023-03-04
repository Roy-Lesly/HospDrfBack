from datetime import datetime
from backdjango.utils import get_access_token, get_query, CustomPagination
from rest_framework import status, generics
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .serializers import (AccountNameSerializer, AccountSerializer, 
    CreateAccountSerializer, LoginSerialiser, UpdatePasswordAccountSerializer, 
    GetAccountSerializer, UpdateAccountSerializer)
from .models import Account, AccountName
from backdjango.custom_methods import IsAuthenticatedCustom
from bcrypt import hashpw, checkpw, gensalt
  

class LoginView(ModelViewSet):
    http_method_names = ["post"]
    queryset = Account.objects.all()
    serializer_class = LoginSerialiser

    def create(self, request):
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)
        new_user = valid_request.validated_data["is_new_user"]
        account = Account.objects.filter(username=valid_request.validated_data["username"])
        if new_user:
            if account:
                account = account[0]
                if not account.password:
                    return Response({"user_id": account.id})
                else:
                    raise Exception("Account has Password Already")
            else:
                return Response(
                    {"error": "User Name or Password Not Found"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if not new_user:
            account = account[0]
            if not account.password:
                raise Exception("Account Has No Password Set")

        account = authenticate(
            username=valid_request.validated_data["username"],
            password=valid_request.validated_data.get("password", None)
        )
        print(valid_request.validated_data["username"])
        
        access = get_access_token({"user_id": account.id}, 1)
        print(access)
        account.last_login = datetime.now()
        account.save()

        return Response({
            "access": access, "user_name": account.username, "user_role": account.role, 
            "user_is_admin": account.is_admin, "dept_name": account.account_name_id.name})


class GetAccountView(ModelViewSet):
    http_method_names = [ "get"]
    queryset = Account.objects.all()
    serializer_class = GetAccountSerializer

    def get_queryset(self):
        # return self.queryset
        return self.queryset.filter(is_superuser=False)


# class CreateAccountView(ModelViewSet):
#     http_method_names = [ "post"]
#     queryset = Account.objects.all()
#     serializer_class = CreateAccountSerializer
    
#     def create(self, request):
#         acc_name = AccountName.objects.filter(id=request.data["account_name_id"])
#         valid_request = self.serializer_class(data=request.data)

#         # request.data["account_name_id"] = acc_name
#         print(request.data, "ACCOUNT VIEW")
#         if Account.objects.filter(username=request.data["username"]):
#             return Response(
#                 {"error": "UserName Exist Already"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         if valid_request.is_valid():
#             print("ACCOUNT VIEW 3")
#             valid_request.save()

#         else:
#             print("ACCOUNT VIEW 4")
#             return Response(
#                 {"error": valid_request.errors},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         return Response(
#             {"success": "Account Created Successfully"},
#             status=status.HTTP_201_CREATED
#         )


class UpdateAccountView(ModelViewSet):
    http_method_names = [ "put", "patch"]
    queryset = Account.objects.all()
    serializer_class = UpdateAccountSerializer

    def partial_update(self, request: Request, pk=None):
        data = request.data
        pwd = data.pop("password", None)
        instance = Account.objects.filter(id=pk).first()
        instance.set_password(pwd)
        data["password"] = instance.password
        serializer = self.serializer_class(data=data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Account Partial Updated Successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(serializer.errors)

    def update(self, request: Request,*args, **kwargs):
        print("UPDATE HERE")
        updated_data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        # Custom update logic goes here
        self.perform_update(serializer)
        print(serializer.data)
        return Response(serializer.data)
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     # Custom update logic goes here
    #     self.perform_update(serializer)
    #     return Response(serializer.data)


    def update1(self, request: Request, pk=None):
        data = request.data
        instance = Account.objects.filter(id=pk).first()
        if data['username'] != "":
            instance.username = data['username']
        if data['role'] != "":
            instance.role = data['role']

        if data['is_admin'] == "":
            instance.is_admin = False
        if data['is_staff'] == "":
            instance.is_staff = False
        if data['is_active'] == "":
            instance.is_active = False
        if data['is_superuser'] == "":
            instance.is_superuser = False

        if data['is_admin'] != "":
            instance.is_admin = data['is_admin']
        if data['is_staff'] != "":
            instance.is_staff = data['is_staff']
        if data['is_active'] != "":
            instance.is_active = data['is_active']
        if data['is_superuser'] != "":
            instance.is_superuser = data['is_superuser']

        if data['password'] != data['password2']:
            raise serializers.ValidationError({'error': "Password Does Not Match"})
        if data['password'] != "":
            instance.set_password(data["password"])
        if data['account_name_id'] == "":
            data['account_name_id'] = instance.account_name_id.id
        
        serializer = self.serializer_class(data=data, instance=instance)
        if serializer.is_valid():
            instance.save()
            response = {
                "message": "Account Updated Successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, instance, pk=None):
        try:
            instance = Account.objects.filter(id=pk).first()
            instance.delete()
            return Response(data={"message": "Account Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={"message": "Account Not Found"}, status=status.HTTP_204_NO_CONTENT)


# class DeleteAccountView(ModelViewSet):
#     http_method_names = ["delete"]
#     queryset = Account.objects.all()

#     def destroy(self, instance, pk=None):
#         instance = self.queryset.filter(id=pk).first()
#         if instance:
#             instance.delete()
#             return Response(data={"message": "Account Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
#         return Response(data={"message": "Account with id[" + pk + "] Not Found !"}, status=status.HTTP_404_NOT_FOUND)


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    
    def list(self, request):
        queryset = Account.objects.filter(is_superuser=False)
        serializer = GetAccountSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        print("CUSTOM CREATE")
        serializer = CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, pk=None):
        queryset = Account.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = AccountSerializer(instance)
        return Response(serializer.data, status=200)
    
    def update(self, request, pk=None):
        queryset = Account.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = UpdateAccountSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def partial_update(self, request, pk=None):
        queryset = Account.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = AccountSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def destroy(self, request, pk=None):
        queryset = Account.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        instance.delete()
        return Response(status=204)


class UpdatePasswordView(ModelViewSet):
    serializer_class = UpdatePasswordAccountSerializer
    http_method_names = ["put"]
    queryset = Account.objects.all()

    def update(self, request, pk=None):
        print(request.data)
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)
        acc_id = valid_request.validated_data["account_id"]
        new_password = valid_request.validated_data["password"]

        account = self.queryset.filter(id=acc_id).first()

        if not account:
            raise Exception("Account with Id not Found")
        account.set_password(new_password)
        account.save()
        return Response({"id": account.id, "username": account.username, "message": "Password Changed Successfully"})


class MeView(ModelViewSet):
    serializer_class = AccountSerializer
    http_method_names = ["get"]
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticatedCustom, )

    def list(self, request):
        print("TEST")
        data1 = Account.objects.get(id=request.user.id)
        user = {
            "id": data1.id,
            "username": data1.username,
            "last_login": data1.last_login,
            "created_at": data1.date_joined,
            "role": data1.role,
            "is_admin": data1.is_admin,
        }
        return Response(user)


class AccountNameView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AccountNameSerializer
    queryset = AccountName.objects.all()
