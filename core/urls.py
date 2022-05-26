from rest_framework.routers import DefaultRouter

from core.views import MachineAPIView, OrderAPIView, ProductAPIView, DecorationInspectionAPIView, \
    PackagingInspectionAPIView, CandleInspectionAPIView

router = DefaultRouter()
app_name = 'core'
router.register('machine', MachineAPIView, basename='machine')
router.register('order', OrderAPIView, basename='order')
router.register('product', ProductAPIView, basename='product')
router.register('decoration_inspection', DecorationInspectionAPIView, basename='decoration_inspection')
router.register('packaging_inspection', PackagingInspectionAPIView, basename='packaging_inspection')
router.register('candle_inspection', CandleInspectionAPIView, basename='candle_inspection')
urlpatterns = router.urls
