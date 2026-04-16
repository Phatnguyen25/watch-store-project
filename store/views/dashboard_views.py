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

def export_orders_excel(request):
    """Xuất danh sách đơn hàng ra file Excel"""
    orders = Order.objects.all().order_by('-created_at')
    
    # Tạo tiêu đề cột
    data = [
        ['Mã Đơn', 'Khách hàng', 'Email', 'SĐT', 'Địa chỉ', 'Tổng Tiền (VNĐ)', 'Trạng Thái', 'Ngày Đặt']
    ]
    
    for o in orders:
        data.append([
            o.id,
            o.full_name,
            o.email,
            o.phone,
            o.address,
            o.total_price,
            o.get_status_display(),
            o.created_at.strftime('%d/%m/%Y %H:%M:%S') if o.created_at else ''
        ])
        
    import django_excel as excel
    return excel.make_response_from_array(data, "xlsx", file_name="danh_sach_don_hang")


# ==========================================
# 1. QUẢN LÝ SẢN PHẨM (PRODUCT CRUD)
# ==========================================
import django_excel as excel

def export_products_excel(request):
    products = Product.objects.all().order_by('id')
    
    # Tạo tiêu đề cột
    data = [
        ['ID', 'Tên sản phẩm', 'ID Danh mục', 'Giá', 'Tồn kho', 'Hiển thị']
    ]
    
    # Nạp dữ liệu
    for p in products:
        data.append([
            p.id,
            p.name,
            p.category_id if p.category_id else '',
            p.price,
            p.stock,
            "Có" if p.is_active else "Không"
        ])
        
    # Trả về file excel
    return excel.make_response_from_array(data, "xlsx", file_name="danh_sach_san_pham")

def import_products_excel(request):
    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            return redirect('store:dashboard_product_list')
            
        try:
            # Lấy dữ liệu dạng mảng dòng
            data = excel_file.get_array()
            
            # Bỏ qua dòng tiêu đề (index 0)
            for row in data[1:]:
                if not row or len(row) < 6:
                    continue
                    
                pid = row[0]
                name = str(row[1]).strip()
                cat_id = row[2]
                price = row[3]
                stock = row[4]
                is_active_str = str(row[5]).strip()
                
                is_active = (is_active_str == "Có")
                
                # Làm sạch dữ liệu rỗng
                if cat_id == '':
                    cat_id = None
                
                if not name:
                    continue
                    
                # Nếu có ID -> Cập nhật (Update)
                if pid:
                    try:
                        p = Product.objects.get(id=int(pid))
                        p.name = name
                        p.category_id = cat_id
                        p.price = price
                        p.stock = stock
                        p.is_active = is_active
                        p.save()
                    except (Product.DoesNotExist, ValueError):
                        pass
                # Nếu không có ID -> Tạo mới (Create)
                else:
                    Product.objects.create(
                        name=name,
                        category_id=cat_id,
                        price=price,
                        stock=stock,
                        is_active=is_active
                    )
        except Exception as e:
            # Nếu có lỗi (ví dụ file sai format)
            pass
            
    return redirect('store:dashboard_product_list')

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

# ==========================================
# 5. BÁO CÁO DOANH THU (REVENUE REPORT)
# ==========================================
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, TruncDay
from django.http import HttpResponse
from django.template.loader import get_template
import datetime

def dashboard_report(request):
    """Trang Báo Cáo Doanh Thu (Hiển thị biểu đồ / bảng)"""
    valid_statuses = ['Processing', 'Shipped', 'Delivered']
    orders = Order.objects.filter(status__in=valid_statuses)
    
    # Doanh thu tháng hiện tại
    now = datetime.datetime.now()
    current_month_orders = orders.filter(created_at__year=now.year, created_at__month=now.month)
    total_revenue_month = current_month_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders_month = current_month_orders.count()
    
    # Chi tiết doanh thu theo ngày trong tháng
    daily_revenue = current_month_orders.annotate(
        date=TruncDay('created_at')
    ).values('date').annotate(
        revenue=Sum('total_price'),
        orders_count=Count('id')
    ).order_by('-date')

    context = {
        'total_revenue_month': total_revenue_month,
        'total_orders_month': total_orders_month,
        'daily_revenue': daily_revenue,
        'current_month': now.strftime('%m/%Y'),
    }
    return render(request, 'store/dashboard/report.html', context)

def export_revenue_excel(request):
    """Xuất file Excel báo cáo doanh thu tháng này"""
    valid_statuses = ['Processing', 'Shipped', 'Delivered']
    now = datetime.datetime.now()
    current_month_orders = Order.objects.filter(status__in=valid_statuses, created_at__year=now.year, created_at__month=now.month)
    
    daily_revenue = current_month_orders.annotate(
        date=TruncDay('created_at')
    ).values('date').annotate(
        revenue=Sum('total_price'),
        orders_count=Count('id')
    ).order_by('date')

    data = [
        ['BÁO CÁO DOANH THU THÁNG ' + now.strftime('%m/%Y')],
        ['Ngày', 'Số đơn hàng thành công', 'Doanh thu (VNĐ)']
    ]
    
    total_rev = 0
    total_ord = 0
    for day in daily_revenue:
        total_rev += day['revenue']
        total_ord += day['orders_count']
        data.append([
            day['date'].strftime('%d/%m/%Y'),
            day['orders_count'],
            float(day['revenue'])
        ])
        
    data.append(['TỔNG CỘNG', total_ord, float(total_rev)])
    
    import django_excel as excel
    return excel.make_response_from_array(data, "xlsx", file_name=f"bao_cao_doanh_thu_{now.strftime('%m_%Y')}")

def export_revenue_pdf(request):
    """Xuất file PDF báo cáo doanh thu"""
    import xhtml2pdf.pisa as pisa
    from io import BytesIO
    
    valid_statuses = ['Processing', 'Shipped', 'Delivered']
    now = datetime.datetime.now()
    current_month_orders = Order.objects.filter(status__in=valid_statuses, created_at__year=now.year, created_at__month=now.month)
    
    daily_revenue = current_month_orders.annotate(
        date=TruncDay('created_at')
    ).values('date').annotate(
        revenue=Sum('total_price'),
        orders_count=Count('id')
    ).order_by('-date')

    total_revenue_month = current_month_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders_month = current_month_orders.count()

    context = {
        'total_revenue_month': total_revenue_month,
        'total_orders_month': total_orders_month,
        'daily_revenue': daily_revenue,
        'current_month': now.strftime('%m/%Y'),
        'export_time': now.strftime('%d/%m/%Y %H:%M:%S')
    }

    template_path = 'store/dashboard/report_pdf.html'
    template = get_template(template_path)
    html  = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bao_cao_doanh_thu_{now.strftime("%m_%Y")}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# ==========================================
# 6. QUẢN LÝ NGƯỜI DÙNG (USER MANAGEMENT)
# ==========================================
from django.contrib.auth.models import User

def dashboard_user_list(request):
    """Hiển thị bảng danh sách toàn bộ người dùng"""
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    
    users = User.objects.all().order_by('-date_joined')
    
    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query))
    
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)
        
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_users = paginator.get_page(page_number)
    
    context = {
        'users': page_users,
        'query': query,
        'status': status
    }
    return render(request, 'store/dashboard/user_list.html', context)

def dashboard_user_update(request, user_id):
    """Admin khóa/mở khóa hoặc sửa thông tin user"""
    target_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'toggle_status':
            # Không cho phép admin khóa chính mình
            if target_user != request.user:
                target_user.is_active = not target_user.is_active
                target_user.save()
        elif action == 'delete_user':
            # Không cho phép tự xóa chính mình và khóa không cho xóa superuser
            if target_user != request.user and not target_user.is_superuser:
                target_user.delete()
        return redirect('store:dashboard_user_list')
        
    # Nếu muốn dùng form edit, có thể truyền form vào đây. Tạm thời render giao diện liệt kê nhỏ
    return redirect('store:dashboard_user_list')