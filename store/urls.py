from django.urls import path
from django.contrib.auth.decorators import user_passes_test

# NHÌN KỸ DÒNG NÀY: Phải import đích danh cart_views
from .views import product_views, store_views, dashboard_views, cart_views, order_views, auth_views, user_views 
from django.contrib.auth import views as dj_auth_views

# Phân quyền: Cấm tài khoản không phải là nhân viên hoặc Admin
def is_staff_check(user):
    return user.is_active and user.is_staff

staff_required = user_passes_test(is_staff_check, login_url='store:login')

app_name = 'store'
urlpatterns = [
    # --- DASHBOARD ---
    path('dashboard/', staff_required(dashboard_views.dashboard_home), name='dashboard_home'),
    path('dashboard/products/', staff_required(dashboard_views.dashboard_product_list), name='dashboard_product_list'),
    path('dashboard/products/export/', staff_required(dashboard_views.export_products_excel), name='export_products_excel'),
    path('dashboard/products/import/', staff_required(dashboard_views.import_products_excel), name='import_products_excel'),
    
    # --- AUTHENTICATION ---
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='register'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('profile/', user_views.profile_view, name='profile'),
    path('activate/<uidb64>/<token>/', auth_views.activate_account, name='activate'),
    
    # --- PASSWORD RESET FLOW ---
    path('password_reset/', dj_auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        success_url='done/'
    ), name='password_reset'),
    path('password_reset/done/', dj_auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', dj_auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', dj_auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # --- TRANG CHỦ & SẢN PHẨM ---
    path('', product_views.product_list, name='product_list'),
    path('products/', product_views.all_products, name='all_products'),
    path('category/<slug:slug>/', product_views.category_products, name='category_products'),
    path('product/<int:pk>/', product_views.product_detail, name='product_detail'),
    path('dashboard/stores/', staff_required(dashboard_views.dashboard_store_list), name='dashboard_store_list'),
    path('dashboard/products/add/', staff_required(dashboard_views.product_create), name='product_create'),
    path('dashboard/products/edit/<int:pk>/', staff_required(dashboard_views.product_update), name='product_update'),
    path('dashboard/products/delete/<int:pk>/', staff_required(dashboard_views.product_delete), name='product_delete'),
    path('dashboard/stores/add/', staff_required(dashboard_views.store_create), name='store_create'),
    path('dashboard/stores/edit/<int:pk>/', staff_required(dashboard_views.store_update), name='store_update'),
    path('dashboard/stores/delete/<int:pk>/', staff_required(dashboard_views.store_delete), name='store_delete'),

    # --- BẢN ĐỒ ---
    path('store-locator/', store_views.store_locator, name='store_locator'),
    path('api/find-nearest/', store_views.api_find_nearest_store, name='api_find_nearest'),
    
    # --- MẴ GIẢM GIÁ ---
    path('dashboard/coupons/', staff_required(dashboard_views.dashboard_coupon_list), name='dashboard_coupon_list'),
    path('dashboard/coupons/add/', staff_required(dashboard_views.coupon_create), name='coupon_create'),
    path('dashboard/coupons/edit/<int:pk>/', staff_required(dashboard_views.coupon_update), name='coupon_update'),
    path('dashboard/coupons/delete/<int:pk>/', staff_required(dashboard_views.coupon_delete), name='coupon_delete'),
        
    # --- DANH MỤC ---
    path('dashboard/categories/', staff_required(dashboard_views.dashboard_category_list), name='dashboard_category_list'),
    path('dashboard/categories/add/', staff_required(dashboard_views.category_create), name='category_create'),
    path('dashboard/categories/edit/<int:pk>/', staff_required(dashboard_views.category_update), name='category_update'),
    path('dashboard/categories/delete/<int:pk>/', staff_required(dashboard_views.category_delete), name='category_delete'),
    
    # --- GIỎ HÀNG (Đã sửa views -> cart_views) ---
    path('cart/', cart_views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', cart_views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/<str:action>/', cart_views.update_cart, name='update_cart'),
    path('checkout/', cart_views.checkout, name='checkout'),
    path('checkout/success/', cart_views.checkout_success, name='checkout_success'),
    
    # --- THANH TOÁN (PAYMENT) ---
    path('payment/create/<int:order_id>/', cart_views.payment_create, name='payment_create'),
    path('payment/return/', cart_views.payment_return, name='payment_return'),
    
    # --- ĐƠN HÀNG (USER & DASHBOARD) ---
    path('orders/', order_views.order_list, name='order_list'),
    path('orders/<int:order_id>/', order_views.order_detail, name='order_detail'),
    path('dashboard/orders/', staff_required(dashboard_views.dashboard_order_list), name='dashboard_order_list'),
    path('dashboard/orders/edit/<int:pk>/', staff_required(dashboard_views.dashboard_order_update), name='dashboard_order_update'),
    path('dashboard/orders/export/', staff_required(dashboard_views.export_orders_excel), name='export_orders_excel'),
    
    # --- BÁO CÁO (REPORT) ---
    path('dashboard/reports/', staff_required(dashboard_views.dashboard_report), name='dashboard_report'),
    path('dashboard/reports/export/excel/', staff_required(dashboard_views.export_revenue_excel), name='export_revenue_excel'),
    path('dashboard/reports/export/pdf/', staff_required(dashboard_views.export_revenue_pdf), name='export_revenue_pdf'),
    
    # --- NGƯỜI DÙNG DASHBOARD ---
    path('dashboard/users/', staff_required(dashboard_views.dashboard_user_list), name='dashboard_user_list'),
    path('dashboard/users/<int:user_id>/update/', staff_required(dashboard_views.dashboard_user_update), name='dashboard_user_update'),
]