from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from store.models import Product, Store, Category, Coupon, Order, OrderItem, StockHistory
from store.forms import ProductForm, StoreForm, CategoryForm, CouponForm, OrderForm
import django_excel as excel

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

    # Nếu là yêu cầu AJAX từ Live-search
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/dashboard/product_table_fragment.html', context)

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

    # Nếu là yêu cầu AJAX từ Live-search
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/dashboard/store_table_fragment.html', context)

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

    # Nếu là yêu cầu AJAX từ Live-search
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/dashboard/category_table_fragment.html', context)

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

    # Nếu là yêu cầu AJAX từ Live-search
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/dashboard/coupon_table_fragment.html', context)

    return render(request, 'store/dashboard/coupon_list.html', context)

def dashboard_stock_history(request):
    """View hiển thị lịch sử biến động kho"""
    history_list = StockHistory.objects.all().select_related('product', 'user')
    
    # Filter theo sản phẩm nếu có
    product_id = request.GET.get('product_id')
    if product_id:
        history_list = history_list.filter(product_id=product_id)
        
    paginator = Paginator(history_list, 20)
    page_number = request.GET.get('page')
    history = paginator.get_page(page_number)
    
    return render(request, 'store/dashboard/stock_history.html', {
        'history': history,
        'page_obj': history,
        'products_list': Product.objects.all().only('id', 'name')
    })

def dashboard_stock_history_detail(request, pk):
    """View chi tiết một bản ghi biến động kho"""
    entry = get_object_or_404(StockHistory, pk=pk)
    return render(request, 'store/dashboard/stock_history_detail.html', {'entry': entry})

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
    
    context = {
        'orders': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'q': q,
        'status': status
    }

    # Nếu là yêu cầu AJAX từ Live-search
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/dashboard/order_table_fragment.html', context)

    return render(request, 'store/dashboard/order_list.html', context)

def dashboard_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    # OrderItem liên quan thông qua related_name='items'
    order_items = order.items.all().select_related('product')
    
    # Tính thành tiền cho từng sản phẩm
    for item in order_items:
        item.subtotal = item.price * item.quantity
        
    context = {
        'order': order,
        'order_items': order_items,
        'title': f'Chi tiết Đơn hàng #{order.id}'
    }
    return render(request, 'store/dashboard/order_detail.html', context)

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
        ['ID', 'Tên sản phẩm', 'ID Danh mục', 'Giá', 'Tổng Tồn Kho Hiện Tại']
    ]
    
    # Nạp dữ liệu
    for p in products:
        data.append([
            p.id,
            p.name,
            p.category_id if p.category_id else '',
            p.price,
            p.stock
        ])
        
    # Trả về file excel
    return excel.make_response_from_array(data, "xlsx", file_name="danh_sach_san_pham")

def download_product_template(request):
    """Xuất file Excel mẫu để nhập hàng"""
    data = [
        ['ID (Để trống nếu thêm mới)', 'Tên Sản Phẩm', 'Mã Danh Mục (ID)', 'Giá (VNĐ)', 'Số Lượng Nhập Thêm']
    ]
    # Thêm một dòng ví dụ
    data.append([None, 'Đồng Hồ Ví Dụ 01', 1, 1500000, 10])
    
    return excel.make_response_from_array(data, "xlsx", file_name="mau_nhap_lieu_san_pham")

def import_products_excel(request):
    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            messages.error(request, "Vui lòng chọn file Excel.")
            return redirect('store:dashboard_product_list')
            
        try:
            # Sử dụng trực tiếp pyexcel (thư viện lõi) để đảm bảo độ ổn định cao nhất
            import pyexcel
            file_extension = excel_file.name.split('.')[-1]
            data = pyexcel.get_array(file_content=excel_file.read(), file_type=file_extension)
            
            success_count = 0
            
            for row in data[1:]:
                if not row or len(row) < 5:
                    continue
                    
                pid = row[0]
                name = str(row[1]).strip()
                cat_id = row[2]
                try:
                    price = float(row[3])
                    new_stock = int(row[4])
                except (ValueError, TypeError):
                    continue
                
                if not name: continue
                
                # Logic cập nhật hoặc tạo mới và ghi lịch sử
                try:
                    if pid and str(pid).isdigit():
                        p = Product.objects.get(id=int(pid))
                        old_stock = p.stock
                        p.name = name
                        p.category_id = cat_id if cat_id else None
                        p.price = price
                        p.stock += new_stock  # CỘNG DỒN TỒN KHO
                        p.save()
                        
                        StockHistory.objects.create(
                            product=p,
                            user=request.user,
                            stock_before=old_stock,
                            stock_after=p.stock,
                            change_amount=new_stock,
                            type='Import',
                            note=f"Nhập thêm qua Excel"
                        )
                    else:
                        p = Product.objects.create(
                            name=name,
                            category_id=cat_id if cat_id else None,
                            price=price,
                            stock=new_stock
                        )
                        StockHistory.objects.create(
                            product=p,
                            user=request.user,
                            stock_before=0,
                            stock_after=new_stock,
                            change_amount=new_stock,
                            type='Import',
                            note="Thêm mới qua Excel"
                        )
                    success_count += 1
                except Exception as e:
                    print(f"Error importing row: {e}")
                    continue
            
            messages.success(request, f"Đã nhập thành công {success_count} sản phẩm.")
        except Exception as e:
            messages.error(request, f"Lỗi xử lý file: {str(e)}")
            
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
    old_stock = product.stock
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            p = form.save()
            new_stock = p.stock
            if old_stock != new_stock:
                StockHistory.objects.create(
                    product=p,
                    user=request.user,
                    stock_before=old_stock,
                    stock_after=new_stock,
                    change_amount=new_stock - old_stock,
                    type='Update',
                    note="Cập nhật thủ công tại trang quản trị"
                )
            messages.success(request, f"Cập nhật sản phẩm '{p.name}' thành công.")
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
    orders_qs = Order.objects.filter(status__in=valid_statuses)
    
    # Lấy tham số tháng/năm từ URL, mặc định là hiện tại
    now = datetime.datetime.now()
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))
    
    # Lọc đơn hàng theo tháng/năm đã chọn
    current_month_orders = orders_qs.filter(created_at__year=year, created_at__month=month)
    total_revenue_month = current_month_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders_month = current_month_orders.count()
    
    # Chi tiết doanh thu theo ngày trong tháng
    daily_revenue = current_month_orders.annotate(
        date=TruncDay('created_at')
    ).values('date').annotate(
        revenue=Sum('total_price'),
        orders_count=Count('id')
    ).order_by('-date')

    # Chuẩn bị dữ liệu cho Chart.js
    chart_labels = [day['date'].strftime('%d/%m') for day in reversed(daily_revenue)]
    chart_data = [float(day['revenue']) for day in reversed(daily_revenue)]

    # Lấy 15 đơn hàng gần đây nhất trong tháng
    recent_orders = current_month_orders.order_by('-created_at')[:15]

    # Danh sách năm để lọc (từ 2024 đến năm hiện tại)
    years_range = range(2024, now.year + 1)

    context = {
        'total_revenue_month': total_revenue_month,
        'total_orders_month': total_orders_month,
        'daily_revenue': daily_revenue,
        'current_month': month,
        'current_year': year,
        'display_date': f"{month:02d}/{year}",
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'recent_orders': recent_orders,
        'years_range': years_range,
    }
    return render(request, 'store/dashboard/report.html', context)

def export_revenue_excel(request):
    """Xuất file Excel báo cáo doanh thu theo tháng/năm"""
    valid_statuses = ['Processing', 'Shipped', 'Delivered']
    now = datetime.datetime.now()
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))
    
    current_month_orders = Order.objects.filter(
        status__in=valid_statuses, 
        created_at__year=year, 
        created_at__month=month
    )
    
    daily_revenue = current_month_orders.annotate(
        date=TruncDay('created_at')
    ).values('date').annotate(
        revenue=Sum('total_price'),
        orders_count=Count('id')
    ).order_by('date')

    display_date = f"{month:02d}/{year}"
    data = [
        ['BÁO CÁO DOANH THU THÁNG ' + display_date],
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
    return excel.make_response_from_array(data, "xlsx", file_name=f"bao_cao_doanh_thu_{month:02d}_{year}")

def export_revenue_pdf(request):
    """Xuất file PDF báo cáo doanh thu theo tháng/năm"""
    import xhtml2pdf.pisa as pisa
    from io import BytesIO
    
    valid_statuses = ['Processing', 'Shipped', 'Delivered']
    now = datetime.datetime.now()
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))
    
    current_month_orders = Order.objects.filter(
        status__in=valid_statuses, 
        created_at__year=year, 
        created_at__month=month
    )
    
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
        'current_month': f"{month:02d}/{year}",
        'export_time': now.strftime('%d/%m/%Y %H:%M:%S')
    }

    template_path = 'store/dashboard/report_pdf.html'
    template = get_template(template_path)
    html  = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bao_cao_doanh_thu_{month:02d}_{year}.pdf"'
    
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

    # Nếu là yêu cầu AJAX từ Live-search
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/dashboard/user_table_fragment.html', context)

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