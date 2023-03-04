from rest_framework import serializers
from rest_framework.validators import ValidationError
from xml.dom import ValidationErr
from apps.account.models import Account, AccountName


class AccountNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountName
        fields = ('__all__')


class LoginSerialiser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(required=False)
    is_new_user = serializers.BooleanField(default=False, required=False)


class RegisterAccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'password', 'password2', 'role', 'is_admin', 'account_name_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def save(self):
        print("Acc Serial")
        account = Account(
                username=self.validated_data['username'],
                role=self.validated_data['role'],  
                account_name_id=self.validated_data['account_name_id'],  
            )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        print(account, "ACCOUNT ====================")
        if password != password2:
            raise serializers.ValidationError({'password': "Passwords Do Not Match"})
        account.set_password(password)
        account.save()


class CreateAccountSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        print("Create i CreateAcc Serializer")
        item = Account.objects.create(**validated_data)
        item.save()
        return item

    class Meta:
        model = Account
        fields = ["username", "role", "is_admin", "account_name_id"]


class GetAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        # fields = "__all__"
        fields = ["username", "role", "is_admin", "is_staff", "is_active", "id", "date_joined", "account_name_id"]


class UpdateAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        # fields = "__all__"
        fields = ["account_name_id", "username", "is_admin", "role", "is_staff", "is_superuser", "is_active"]


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = "__all__"


    def validate(self, attrs):
        print("Validate ACCOUNT SERIALIZER")
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Passwords Do Not Match"})
        return super().validate(attrs)

    def create(self, validated_data):
        print("CREATE ACCOUNT SERIALIZER")
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        instance = self.Meta.model(**validated_data)
        if password is None:
            raise serializers.ValidationError({'password': "Password Not Provided"})
        instance.set_password(password)
        instance.save()
        return instance

    def update(self, validated_data):
        print("UPDATE ACCOUNT SERIALIZER")
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        instance = self.Meta.model(**validated_data)
        if password is None:
            raise serializers.ValidationError({'password': "Password Not Provided"})
        instance.set_password(password)
        instance.save()
        return instance
    
    
class UpdatePasswordAccountSerializer(serializers.Serializer):
    account_id = serializers.CharField()
    password = serializers.CharField()