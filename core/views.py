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
    ProductPackagingInspectionSerializer, ProductCandleInspectionSerializer, ProductDataSerializer, \
    OrderedProductSerializer, CandleInspectionImageSerializer, PackagingInspectionImageSerializer, \
    DecorationInspectionImageSerializer


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
        if self.action in ['products']:
            return OrderProductSerializer
        if self.action in ['product']:
            return OrderedProductSerializer
        if self.action == 'decoration_inspection':
            return ProductDecorationInspectionSerializer
        if self.action == 'packaging_inspection':
            return ProductPackagingInspectionSerializer
        if self.action == 'candle_inspection':
            return ProductCandleInspectionSerializer
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

    @action(methods=['GET'], detail=True)
    def products(self, request, pk):
        order = self.get_object()
        return Response(ProductSerializer(order.products, many=True).data)

    @action(methods=['DELETE'], detail=True, url_path=r'product/(?P<product_id>\w+)', )
    def delete_product(self, request, pk, product_id):
        order = self.get_object()
        try:
            product = Product.objects.get(id=product_id)
            order.products.remove(product)
        except:
            pass
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=True)
    def product(self, request, pk):
        order = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for i in serializer.validated_data['products']:
            order.products.add(i)
        order.save()
        return Response(ProductSerializer(order.products, many=True).data, status.HTTP_201_CREATED)

    @action(methods=['GET', 'POST'], detail=True)
    def decoration_inspection(self, request, pk):
        if request.method == 'GET':
            order = self.get_object()
            di = DecorationInspection.objects.filter(order=order)
            return Response(self.get_serializer(di, many=True).data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['order'] = self.get_object()
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

    @action(methods=['GET', 'POST'], detail=True)
    def packaging_inspection(self, request, pk):
        if request.method == 'GET':
            order = self.get_object()
            di = PackagingInspection.objects.filter(order=order)
            return Response(self.get_serializer(di, many=True).data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['order'] = self.get_object()
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

    @action(methods=['GET', 'POST'], detail=True)
    def candle_inspection(self, request, pk):
        if request.method == 'GET':
            order = self.get_object()
            di = CandleInspection.objects.filter(order=order)
            return Response(self.get_serializer(di, many=True).data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['order'] = self.get_object()
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)


class ProductAPIView(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDataSerializer
        else:
            return ProductSerializer


class DecorationInspectionAPIView(viewsets.GenericViewSet,
                                  # mixins.ListModelMixin,
                                  # mixins.CreateModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin):
    queryset = DecorationInspection.objects.all()
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.action in ['image']:
            return DecorationInspectionImageSerializer
        return DecorationInspectionSerializer

    @action(methods=['POST'], detail=True)
    def image(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['decoration_inspection'] = self.get_object()
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class PackagingInspectionAPIView(viewsets.GenericViewSet,
                                 # mixins.ListModelMixin,
                                 # mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin):
    queryset = PackagingInspection.objects.all()
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.action in ['image']:
            return PackagingInspectionImageSerializer
        return PackagingInspectionSerializer

    @action(methods=['POST'], detail=True)
    def image(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['packaging_inspection'] = self.get_object()
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class CandleInspectionAPIView(viewsets.GenericViewSet,
                              # mixins.ListModelMixin,
                              # mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin):
    queryset = CandleInspection.objects.all()
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.action in ['image']:
            return CandleInspectionImageSerializer
        return CandleInspectionSerializer

    @action(methods=['POST'], detail=True)
    def image(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['candle_inspection'] = self.get_object()
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
