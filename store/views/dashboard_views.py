from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Store 
# ĐÃ SỬA: Phải import thêm StoreForm vào đây nhé
from store.forms import ProductForm, StoreForm 

def dashboard_home(request):
    """VIEW ĐỘNG: Lấy số liệu thật từ Database cho trang Tổng quan"""
    total_products = Product.objects.count()
    total_stores = Store.objects.count()
    new_orders = 0 
    revenue = 0

    context = {
        'total_products': total_products,
        'total_stores': total_stores,
        'new_orders': new_orders,
        'revenue': revenue
    }
    return render(request, 'store/dashboard/index.html', context)

def dashboard_product_list(request):
    """VIEW ĐỘNG: Lấy toàn bộ sản phẩm thật"""
    products = Product.objects.all().order_by('-id')
    return render(request, 'store/dashboard/product_list.html', {'products': products})

def dashboard_store_list(request):
    """VIEW ĐỘNG: Lấy toàn bộ cửa hàng thật"""
    stores = Store.objects.all().order_by('-id')
    return render(request, 'store/dashboard/store_list.html', {'stores': stores})

# ==========================================
# QUẢN LÝ SẢN PHẨM (PRODUCT CRUD)
# ==========================================

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_product_list')
    else:
        form = ProductForm()
    return render(request, 'store/dashboard/product_form.html', {'form': form, 'title': 'Thêm Sản Phẩm Mới'})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/dashboard/product_form.html', {'form': form, 'title': f'Sửa Sản Phẩm: {product.name}'})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard_product_list')
    return render(request, 'store/dashboard/product_confirm_delete.html', {'product': product})

# ==========================================
# QUẢN LÝ CỬA HÀNG (STORE CRUD) - MỚI THÊM
# ==========================================

def store_create(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_store_list')
    else:
        form = StoreForm()
    # Dùng chung giao diện product_form.html cho lẹ, chỉ cần đổi title
    return render(request, 'store/dashboard/product_form.html', {'form': form, 'title': 'Thêm Cửa Hàng Mới'})

def store_update(request, pk):
    store_obj = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store_obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard_store_list')
    else:
        form = StoreForm(instance=store_obj)
    return render(request, 'store/dashboard/product_form.html', {'form': form, 'title': f'Sửa Cửa Hàng: {store_obj.name}'})

def store_delete(request, pk):
    store_obj = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        store_obj.delete()
        return redirect('dashboard_store_list')
    # Dùng chung giao diện confirm_delete của Product
    return render(request, 'store/dashboard/product_confirm_delete.html', {'product': store_obj})