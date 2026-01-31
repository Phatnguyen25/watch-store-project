from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin  # Import giao diện bản đồ
from django_json_widget.widgets import JSONEditorWidget # Import giao diện sửa JSON
from django.db import models
from .models import Category, Product, Store

# 1. Quản lý Danh mục
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} # Tự động tạo slug từ tên

# 2. Quản lý Sản phẩm (Có giao diện JSON đẹp)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name',)
    list_filter = ('category',)
    
    # Cấu hình để nhập JSONField bằng giao diện đẹp thay vì text thường
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

# 3. Quản lý Cửa hàng (Có bản đồ để chấm điểm)
@admin.register(Store)
class StoreAdmin(LeafletGeoAdmin): 
    list_display = ('name', 'address')
    # LeafletGeoAdmin sẽ tự hiện bản đồ khi bạn thêm/sửa cửa hàng