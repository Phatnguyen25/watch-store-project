from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from store.models import Product, Store, Category, Coupon
from store.models.order import Order
from store.forms import ProductForm, StoreForm, CategoryForm, CouponForm, OrderForm

def dashboard_home(request):
    """VIEW ĐỘNG: Lấy số liệu thật từ Database cho trang Tổng quan"""
    total_products = Product.objects.count()
    total_stores = Store.objects.count()
    total_categories = Category.objects.count()
    total_coupons = Coupon.objects.count()
    total_orders = Order.objects.count()

    context = {
        'total_products': total_products,
        'total_stores': total_stores,
        'total_categories': total_categories,
        'total_coupons': total_coupons,
        'total_orders': total_orders,
    }
    return render(request, 'store/dashboard/index.html', context)

def dashboard_product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category_id', '')
    status = request.GET.get('status', '') # Thêm filter is_active
    
    products_list = Product.objects.all().order_by('-id')
    categories = Category.objects.all() # Gửi danh sách Category ra UI

    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
    if category_id:
        products_list = products_list.filter(category_id=category_id)
        
    if status == 'active':
        products_list = products_list.filter(is_active=True)
    elif status == 'inactive':
        products_list = products_list.filter(is_active=False)

    paginator = Paginator(products_list, 20)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'query': query,
        'category_id': category_id,
        'status': status,
        'categories': categories,
    }
    return render(request, 'store/dashboard/product_list.html', context)

def dashboard_store_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '') # Lọc theo hoạt động
    
    stores_list = Store.objects.all().order_by('name')

    if query:
        stores_list = stores_list.filter(
            Q(name__icontains=query) | Q(address__icontains=query)
        )
        
    if status == 'active':
        stores_list = stores_list.filter(is_active=True)
    elif status == 'inactive':
        stores_list = stores_list.filter(is_active=False)

    paginator = Paginator(stores_list, 20)
    page_number = request.GET.get('page')
    stores = paginator.get_page(page_number)

    context = {
        'stores': stores,
        'query': query,
        'status': status,
    }
    return render(request, 'store/dashboard/store_list.html', context)

def dashboard_category_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '') # Lọc active
    
    categories_list = Category.objects.all().order_by('name')

    if query:
        categories_list = categories_list.filter(name__icontains=query)
        
    if status == 'active':
        categories_list = categories_list.filter(active=True)
    elif status == 'inactive':
        categories_list = categories_list.filter(active=False)

    paginator = Paginator(categories_list, 20)
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'query': query,
        'status': status,
    }
    return render(request, 'store/dashboard/category_list.html', context)

def dashboard_coupon_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '') # Lọc active
    
    coupons_list = Coupon.objects.all().order_by('-valid_to')

    if query:
        coupons_list = coupons_list.filter(code__icontains=query)
        
    if status == 'active':
        coupons_list = coupons_list.filter(active=True)
    elif status == 'inactive':
        coupons_list = coupons_list.filter(active=False)

    paginator = Paginator(coupons_list, 20)
    page_number = request.GET.get('page')
    coupons = paginator.get_page(page_number)

    context = {
        'coupons': coupons,
        'query': query,
        'status': status,
    }
    return render(request, 'store/dashboard/coupon_list.html', context)

def dashboard_order_list(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    
    orders = Order.objects.all().order_by('-created_at')
    if q:
        orders = orders.filter(Q(full_name__icontains=q) | Q(phone__icontains=q) | Q(id__icontains=q))
    if status:
        orders = orders.filter(status=status)
        
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/dashboard/order_list.html', {
        'orders': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'q': q,
        'status': status
    })

def dashboard_order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('store:dashboard_order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'store/dashboard/general_form.html', {'form': form, 'title': f'Sửa Đơn Hàng #{order.id}'})


# ==========================================
# 1. QUẢN LÝ SẢN PHẨM (PRODUCT CRUD)
# ==========================================
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store:dashboard_product_list') # Đã sửa namespace
    else:
        form = ProductForm()
    return render(request, 'store/dashboard/general_form.html', {'form': form, 'title': 'Thêm Sản Phẩm Mới'})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('store:dashboard_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/dashboard/general_form.html', {'form': form, 'title': f'Sửa Sản Phẩm: {product.name}'})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('store:dashboard_product_list')
    return render(request, 'store/dashboard/product_confirm_delete.html', {'object': product}) # Đã sửa thành object


# ==========================================
# 2. QUẢN LÝ CỬA HÀNG (STORE CRUD)
# ==========================================
def store_create(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:dashboard_store_list')
    else:
        form = StoreForm()
    return render(request, 'store/dashboard/general_form.html', {'form': form, 'title': 'Thêm Cửa Hàng Mới'})

def store_update(request, pk):
    store_obj = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store_obj)
        if form.is_valid():
            form.save()
            return redirect('store:dashboard_store_list')
    else:
        form = StoreForm(instance=store_obj)
    return render(request, 'store/dashboard/general_form.html', {'form': form, 'title': f'Sửa Cửa Hàng: {store_obj.name}'})

def store_delete(request, pk):
    store_obj = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        store_obj.delete()
        return redirect('store:dashboard_store_list')
    return render(request, 'store/dashboard/product_confirm_delete.html', {'object': store_obj})


# ==========================================
# 3. QUẢN LÝ DANH MỤC (CATEGORY CRUD)
# ==========================================
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:dashboard_category_list')
    else:
        form = CategoryForm()
    return render(request, 'store/dashboard/general_form.html', {'form': form, 'title': 'Thêm Danh Mục Mới'})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('store:dashboard_category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'store/dashboard/general_form.html', {'form': form, 'title': f'Sửa Danh Mục: {category.name}'})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('store:dashboard_category_list')
    return render(request, 'store/dashboard/product_confirm_delete.html', {'object': category})


# ==========================================
# 4. QUẢN LÝ MÃ GIẢM GIÁ (COUPON CRUD)
# ==========================================
def coupon_create(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:dashboard_coupon_list')
    else:
        form = CouponForm()
    return render(request, 'store/dashboard/general_form.html', {'form': form, 'title': 'Tạo Mã Giảm Giá Mới'})

def coupon_update(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('store:dashboard_coupon_list')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'store/dashboard/general_form.html', {'form': form, 'title': f'Sửa Mã: {coupon.code}'})

def coupon_delete(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        coupon.delete()
        return redirect('store:dashboard_coupon_list')
    return render(request, 'store/dashboard/general_confirm_delete.html', {'object': coupon})