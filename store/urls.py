from django.urls import path

# NHÌN KỸ DÒNG NÀY: Phải import đích danh cart_views
from .views import product_views, store_views, dashboard_views, cart_views 

app_name = 'store'
urlpatterns = [
    # --- DASHBOARD ---
    path('dashboard/', dashboard_views.dashboard_home, name='dashboard_home'),
    path('dashboard/products/', dashboard_views.dashboard_product_list, name='dashboard_product_list'),
    
    # --- TRANG CHỦ & SẢN PHẨM ---
    path('', product_views.product_list, name='product_list'),          
    path('product/<int:pk>/', product_views.product_detail, name='product_detail'),
    path('dashboard/stores/', dashboard_views.dashboard_store_list, name='dashboard_store_list'),
    path('dashboard/products/add/', dashboard_views.product_create, name='product_create'),
    path('dashboard/products/edit/<int:pk>/', dashboard_views.product_update, name='product_update'),
    path('dashboard/products/delete/<int:pk>/', dashboard_views.product_delete, name='product_delete'),
    path('dashboard/stores/add/', dashboard_views.store_create, name='store_create'),
    path('dashboard/stores/edit/<int:pk>/', dashboard_views.store_update, name='store_update'),
    path('dashboard/stores/delete/<int:pk>/', dashboard_views.store_delete, name='store_delete'),

    # --- BẢN ĐỒ ---
    path('store-locator/', store_views.store_locator, name='store_locator'),
    path('api/find-nearest/', store_views.api_find_nearest_store, name='api_find_nearest'),
    
    # --- GIỎ HÀNG (Đã sửa views -> cart_views) ---
    path('cart/', cart_views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', cart_views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/<str:action>/', cart_views.update_cart, name='update_cart'),
    path('checkout/', cart_views.checkout, name='checkout'),
    path('cart/update/<int:item_id>/<str:action>/', cart_views.update_cart, name='update_cart'),
    path('checkout/success/', cart_views.checkout_success, name='checkout_success'),
]