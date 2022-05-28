from django.contrib.auth.models import User
# Create your views here.
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import Machine, Order, Product, DecorationInspection, PackagingInspection, CandleInspection
from core.serializer import UserSerializer, JWTObtainPairSerializer, MachineSerializer, OrderSerializer, \
    ProductSerializer, DecorationInspectionSerializer, PackagingInspectionSerializer, CandleInspectionSerializer, \
    OrderCreateSerializer, OrderProductSerializer, ProductDecorationInspectionSerializer, \
    ProductPackagingInspectionSerializer, ProductCandleInspectionSerializer, ProductDataSerializer


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

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return OrderCreateSerializer
        if self.action in ['product']:
            return OrderProductSerializer
        else:
            return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.create(user=self.request.user,
                                     client_name=serializer.validated_data['client_name'],
                                     order_number=serializer.validated_data['order_number'],
                                     manufacture_order=serializer.validated_data['manufacture_order'],
                                     status=serializer.validated_data['status'],
                                     machine_id=serializer.validated_data['machine_id'])
        order.save()
        return Response(OrderSerializer(order, many=False).data, status=status.HTTP_201_CREATED)

    @action(methods=['GET', 'POST'], detail=True)
    def product(self, request, pk):
        if request.method == 'GET':
            order = self.get_object()
            products = Product.objects.filter(order=order)
            return Response(ProductSerializer(products, many=True).data)
        else:
            request.data['order'] = self.get_object().id
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)


class ProductAPIView(viewsets.GenericViewSet,
                     # mixins.ListModelMixin,
                     # mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Product.objects.all()

    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.action == 'decoration_inspection':
            return ProductDecorationInspectionSerializer
        if self.action == 'packaging_inspection':
            return ProductPackagingInspectionSerializer
        if self.action == 'candle_inspection':
            return ProductCandleInspectionSerializer
        if self.action == 'retrieve':
            return ProductDataSerializer
        else:
            return ProductSerializer

    @action(methods=['GET', 'POST'], detail=True)
    def decoration_inspection(self, request, pk):
        if request.method == 'GET':
            product = self.get_object()
            di = DecorationInspection.objects.filter(product=product)
            return Response(self.get_serializer(di, many=True).data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['product'] = self.get_object()
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

    @action(methods=['GET', 'POST'], detail=True)
    def packaging_inspection(self, request, pk):
        if request.method == 'GET':
            product = self.get_object()
            di = PackagingInspection.objects.filter(product=product)
            return Response(self.get_serializer(di, many=True).data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['product'] = self.get_object()
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

    @action(methods=['GET', 'POST'], detail=True)
    def candle_inspection(self, request, pk):
        if request.method == 'GET':
            product = self.get_object()
            di = CandleInspection.objects.filter(product=product)
            return Response(self.get_serializer(di, many=True).data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['product'] = self.get_object()
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)


class DecorationInspectionAPIView(viewsets.GenericViewSet,
                                  # mixins.ListModelMixin,
                                  # mixins.CreateModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin):
    queryset = DecorationInspection.objects.all()
    serializer_class = DecorationInspectionSerializer
    parser_classes = [MultiPartParser]


class PackagingInspectionAPIView(viewsets.GenericViewSet,
                                 # mixins.ListModelMixin,
                                 # mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin):
    queryset = PackagingInspection.objects.all()
    serializer_class = PackagingInspectionSerializer
    parser_classes = [MultiPartParser]


class CandleInspectionAPIView(viewsets.GenericViewSet,
                              # mixins.ListModelMixin,
                              # mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin):
    queryset = CandleInspection.objects.all()
    serializer_class = CandleInspectionSerializer
    parser_classes = [MultiPartParser]
