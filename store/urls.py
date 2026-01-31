# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Đường dẫn trang chủ (Danh sách sản phẩm)
    path('', views.product_list, name='product_list'),

    # Đường dẫn trang chi tiết (Ví dụ: /product/1/)
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]