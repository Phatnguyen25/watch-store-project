from django.shortcuts import render, get_object_or_404
from store.models import Product, Category

def product_list(request):
    """Trang danh sách sản phẩm (lấy từ Database)"""
    products = Product.objects.all()
    return render(request, 'store/product/list.html', {'products': products})

def product_detail(request, pk):
    """Trang chi tiết 1 sản phẩm (lấy từ Database)"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product/details.html', {'product': product})