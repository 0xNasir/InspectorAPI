from django.contrib.auth.models import User
# Create your views here.
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import Machine, Order, Product, DecorationInspection, PackagingInspection, CandleInspection
from core.serializer import UserSerializer, JWTObtainPairSerializer, MachineSerializer, OrderSerializer, \
    ProductSerializer, DecorationInspectionSerializer, PackagingInspectionSerializer, CandleInspectionSerializer


class RegisterAPIView(viewsets.GenericViewSet,
                      mixins.CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(first_name=serializer.validated_data['first_name'],
                                   last_name=serializer.validated_data['last_name'],
                                   email=serializer.validated_data['email'],
                                   username=serializer.validated_data['username'])
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = JWTObtainPairSerializer


class MachineAPIView(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


class OrderAPIView(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ProductAPIView(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DecorationInspectionAPIView(viewsets.GenericViewSet,
                                  mixins.ListModelMixin,
                                  mixins.CreateModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin):
    queryset = DecorationInspection.objects.all()
    serializer_class = DecorationInspectionSerializer


class PackagingInspectionAPIView(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin):
    queryset = PackagingInspection.objects.all()
    serializer_class = PackagingInspectionSerializer


class CandleInspectionAPIView(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin):
    queryset = CandleInspection.objects.all()
    serializer_class = CandleInspectionSerializer
