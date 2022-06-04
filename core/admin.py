from django.contrib import admin

# Register your models here.
from core.models import Machine, Order, Product, DecorationInspection, PackagingInspection, CandleInspection, \
    CandleInspectionImage, PackagingInspectionImage, DecorationInspectionImage


class MachineAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_enabled', 'created_at', 'modified_at']
    search_fields = ['machine_name']
    list_filter = ['is_enabled', 'created_at', 'modified_at']
    list_per_page = 20


admin.site.register(Machine, MachineAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'order_number', 'machine_id', 'status']
    search_fields = ['client_name']
    list_filter = ['created_at', 'modified_at']
    list_per_page = 20


admin.site.register(Order, OrderAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'product_id', 'product_type', 'is_enable']
    search_fields = ['name']
    list_filter = ['is_enable', 'created_at', 'modified_at']
    list_per_page = 20


admin.site.register(Product, ProductAdmin)


class DecorationInspectionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'decoration_type']
    search_fields = ['product.name']
    list_filter = ['decoration_type', 'created_at', 'modified_at']
    list_per_page = 20


admin.site.register(DecorationInspection, DecorationInspectionAdmin)


class PackagingInspectionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'packaging_type']
    search_fields = ['product.name']
    list_filter = ['packaging_type', 'created_at', 'modified_at']
    list_per_page = 20


admin.site.register(PackagingInspection, PackagingInspectionAdmin)


class CandleInspectionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'candle_type']
    search_fields = ['product.name']
    list_filter = ['candle_type', 'created_at', 'modified_at']
    list_per_page = 20


admin.site.register(CandleInspection, CandleInspectionAdmin)

admin.site.register(DecorationInspectionImage)
admin.site.register(PackagingInspectionImage)
admin.site.register(CandleInspectionImage)
