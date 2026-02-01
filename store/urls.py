# store/urls.py
from django.urls import path
from .views import product_views, store_views

urlpatterns = [
    # Đường dẫn trang chủ (Danh sách sản phẩm)
    path('', product_views.product_list, name='product_list'),          

    # Đường dẫn trang chi tiết (Ví dụ: /product/1/)
    path('product/<int:pk>/', product_views.product_detail, name='product_detail'),

    path('store-locator/', store_views.store_locator, name='store_locator'),
    path('api/find-nearest/', store_views.api_find_nearest_store, name='api_find_nearest'),

]