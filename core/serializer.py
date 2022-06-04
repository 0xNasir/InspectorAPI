from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import Machine, Order, Product, DecorationInspection, PackagingInspection, CandleInspection, \
    CandleInspectionImage, PackagingInspectionImage, DecorationInspectionImage


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


class OrderCreateSerializer(ModelSerializer):
    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class DecorationInspectionSerializer(ModelSerializer):
    class Meta:
        model = DecorationInspection
        fields = '__all__'


class DecorationInspectionImageSerializer(ModelSerializer):
    class Meta:
        model = DecorationInspectionImage
        fields = ['id', 'image']


class ProductDecorationInspectionSerializer(ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    decoration_inspection_image = DecorationInspectionImageSerializer(many=True, read_only=True)

    class Meta:
        model = DecorationInspection
        fields = '__all__'


class PackagingInspectionSerializer(ModelSerializer):
    class Meta:
        model = PackagingInspection
        fields = '__all__'


class PackagingInspectionImageSerializer(ModelSerializer):
    class Meta:
        model = PackagingInspectionImage
        fields = ['id', 'image']


class ProductPackagingInspectionSerializer(ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    packaging_inspection_image = PackagingInspectionImageSerializer(many=True, read_only=True)

    class Meta:
        model = PackagingInspection
        fields = '__all__'


class CandleInspectionSerializer(ModelSerializer):
    class Meta:
        model = CandleInspection
        fields = '__all__'


class CandleInspectionImageSerializer(ModelSerializer):
    class Meta:
        model = CandleInspectionImage
        fields = ['id', 'image']


class ProductCandleInspectionSerializer(ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    candle_inspection_image = CandleInspectionImageSerializer(many=True, read_only=True)

    class Meta:
        model = CandleInspection
        fields = '__all__'


class ProductDataSerializer(ModelSerializer):
    product_decoration_inspection = DecorationInspectionSerializer(many=True)
    product_packaging_inspection = PackagingInspectionSerializer(many=True)
    product_candle_inspection = CandleInspectionSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class OrderedProductSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['products']
