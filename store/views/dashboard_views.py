from django.shortcuts import render, redirect, get_object_or_404
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
    products = Product.objects.all().order_by('-id')
    return render(request, 'store/dashboard/product_list.html', {'products': products})

def dashboard_store_list(request):
    stores = Store.objects.all().order_by('-id')
    return render(request, 'store/dashboard/store_list.html', {'stores': stores})

def dashboard_category_list(request):
    categories = Category.objects.all().order_by('-id')
    return render(request, 'store/dashboard/category_list.html', {'categories': categories})

def dashboard_coupon_list(request):
    coupons = Coupon.objects.all().order_by('-id')
    return render(request, 'store/dashboard/coupon_list.html', {'coupons': coupons})

def dashboard_order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'store/dashboard/order_list.html', {'orders': orders})

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