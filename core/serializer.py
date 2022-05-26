from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import Machine, Order, Product, DecorationInspection, PackagingInspection, CandleInspection


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])


class JWTObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['email'] = user.email
        return token


class MachineSerializer(ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class DecorationInspectionSerializer(ModelSerializer):
    class Meta:
        model = DecorationInspection
        fields = '__all__'


class PackagingInspectionSerializer(ModelSerializer):
    class Meta:
        model = PackagingInspection
        fields = '__all__'

class CandleInspectionSerializer(ModelSerializer):
    class Meta:
        model = CandleInspection
        fields = '__all__'
