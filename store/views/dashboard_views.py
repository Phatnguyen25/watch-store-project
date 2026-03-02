from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from store.models.product import Product
from store.models.store import Store

# Decorator này bảo vệ trang: Chỉ tài khoản Admin (is_staff=True) mới vào được
@staff_member_required(login_url='/') 
def dashboard_home(request):
    """Trang chủ của Admin thống kê tổng quan"""
    total_products = Product.objects.count()
    total_stores = Store.objects.count()
    
    context = {
        'total_products': total_products,
        'total_stores': total_stores,
    }
    return render(request, 'store/dashboard/index.html', context)

@staff_member_required(login_url='/')
def dashboard_product_list(request):
    """Trang danh sách sản phẩm trong Admin"""
    products = Product.objects.all().order_by('-id')
    return render(request, 'store/dashboard/product_list.html', {'products': products})