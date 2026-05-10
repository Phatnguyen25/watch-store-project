from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from store.models import Product, Coupon
from store.models.order import Order, OrderItem
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from decimal import Decimal

def get_cart_data(request):
    """Hàm bổ trợ: Tính toán dữ liệu giỏ hàng từ Session hoặc Database"""
    cart_items = []
    cart_total = 0

    if request.user.is_authenticated:
        from store.models import CartItem
        db_items = CartItem.objects.filter(user=request.user).select_related('product')
        for item in db_items:
            total_price = item.product.price * item.quantity
            cart_total += total_price
            cart_items.append({
                'item_id': item.product.id, # Khớp với Template
                'product_id': item.product.id,
                'name': item.product.name,
                'price': item.product.price,
                'quantity': item.quantity,
                'total': total_price,
                'image': item.product.image.url if item.product.image else None,
            })
    else:
        cart = request.session.get('cart', {})
        for product_id_str, quantity in cart.items():
            try:
                product = Product.objects.get(id=int(product_id_str))
                total_price = product.price * quantity
                cart_total += total_price
                
                cart_items.append({
                    'item_id': product.id,
                    'product_id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': quantity,
                    'total': total_price,
                    'image': product.image.url if product.image else None,
                })
            except Product.DoesNotExist:
                continue
            
    # Lưu tổng tiền vào session để các hàm khác (như apply_coupon) sử dụng
    request.session['cart_total'] = float(cart_total)
    return cart_items, cart_total

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        from store.models import CartItem, Product
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        cart[product_id_str] = cart.get(product_id_str, 0) + 1
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect('store:cart_detail')

def cart_detail(request):
    cart_items, cart_total = get_cart_data(request)
    
    # Khởi tạo các giá trị mặc định
    discount_amount = 0
    discount_percent = 0
    coupon_code = ""

    # Xử lý áp dụng mã giảm giá (Coupon) qua POST
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code', '').strip()
        if coupon_code:
            try:
                from store.models import Coupon
                coupon = Coupon.objects.get(code__iexact=coupon_code, active=True)
                discount_percent = coupon.discount_percent
                discount_amount = (cart_total * discount_percent) / 100
                
                # Lưu vào session để dùng cho trang Checkout
                request.session['coupon_id'] = coupon.id
                request.session['discount_amount'] = float(discount_amount)
                request.session['discount_percent'] = discount_percent
                
                from django.contrib import messages
                messages.success(request, f"Đã áp dụng mã giảm giá: {coupon.code} (-{discount_percent}%)")
            except Coupon.DoesNotExist:
                from django.contrib import messages
                messages.error(request, "Mã giảm giá không tồn tại hoặc đã hết hạn.")
                # Xóa thông tin giảm giá cũ nếu mã mới sai
                request.session.pop('coupon_id', None)
                request.session.pop('discount_amount', None)
                request.session.pop('discount_percent', None)
    else:
        # Nếu là GET, kiểm tra xem đã có mã trong session chưa để hiển thị lại
        # Luôn ép kiểu Decimal để tính toán an toàn
        discount_amount = Decimal(str(request.session.get('discount_amount', 0)))
        discount_percent = request.session.get('discount_percent', 0)

    final_total = cart_total - Decimal(str(discount_amount))

    return render(request, 'store/cart/cart_detail.html', {
        'cart_items': cart_items, 
        'sub_total': cart_total,      # Đồng bộ với Template
        'discount_amount': discount_amount,
        'discount_percent': discount_percent,
        'final_total': final_total    # Đồng bộ với Template
    })

def update_cart(request, item_id, action):
    if request.user.is_authenticated:
        from store.models import CartItem
        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=item_id)
            if action == 'increase':
                cart_item.quantity += 1
                cart_item.save()
            elif action == 'decrease':
                cart_item.quantity -= 1
                if cart_item.quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.save()
        except CartItem.DoesNotExist:
            pass
    else:
        cart = request.session.get('cart', {})
        item_id_str = str(item_id)
        
        if item_id_str in cart:
            if action == 'increase':
                cart[item_id_str] += 1
            elif action == 'decrease':
                cart[item_id_str] -= 1
                if cart[item_id_str] <= 0:
                    del cart[item_id_str]
            
            request.session['cart'] = cart
            request.session.modified = True
            
    return redirect('store:cart_detail')

def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        from store.models import CartItem
        CartItem.objects.filter(user=request.user, product_id=item_id).delete()
    else:
        cart = request.session.get('cart', {})
        item_id_str = str(item_id)
        if item_id_str in cart:
            del cart[item_id_str]
            request.session['cart'] = cart
            request.session.modified = True
            
    return redirect('store:cart_detail')

# --- LOGIC MÃ GIẢM GIÁ (MỚI) ---
def apply_coupon(request):
    code = request.GET.get('code')
    # Lấy tổng tiền từ hàm get_cart_data đã lưu vào session
    total = float(request.session.get('cart_total', 0))
    
    try:
        coupon = Coupon.objects.get(code__iexact=code, active=True)
        discount = (total * coupon.discount_percent) / 100
        new_total = total - discount
        
        # Lưu thông tin giảm giá vào session để lúc tạo Order thật sẽ dùng
        request.session['coupon_id'] = coupon.id
        request.session['discount_amount'] = float(discount)
        
        return JsonResponse({
            'success': True,
            'discount': discount,
            'new_total': new_total,
            'message': f'Áp dụng mã {coupon.code} thành công (-{coupon.discount_percent}%)'
        })
    except Coupon.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Mã giảm giá không hợp lệ!'})

@login_required(login_url='store:login')
def checkout(request):
    cart_items, cart_total = get_cart_data(request)
    
    # Lấy thông tin giảm giá từ session (đã áp dụng ở trang giỏ hàng)
    # Ép kiểu Decimal để tránh lỗi TypeError khi tính toán với cart_total
    discount_amount = Decimal(str(request.session.get('discount_amount', 0)))
    final_total = max(Decimal('0'), cart_total - discount_amount)
    
    if not cart_items:
        # Nếu không có sản phẩm nào trong giỏ (từ DB hoặc session), quay về trang chủ
        return redirect('store:product_list')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        user = request.user
        
        # Tạo đơn hàng với giá tiền thực tế ĐÃ GIẢM
        order = Order.objects.create(
            user=user,
            email=user.email,
            full_name=full_name,
            phone=phone,
            address=address,
            total_price=final_total,
            status='Pending'
        )
        
        from django.db.models import F
        for item in cart_items:
            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                price=item['price'],
                quantity=item['quantity']
            )
            
            # Khắc phục lỗi: Trừ số lượng tồn kho an toàn
            Product.objects.filter(id=product.id).update(stock=F('stock') - item['quantity'])
            
        # Clean Cart Session / Database
        if request.user.is_authenticated:
            from store.models import CartItem
            CartItem.objects.filter(user=request.user).delete()
        else:
            request.session['cart'] = {}
            request.session.modified = True
        
        # Gửi email hóa đơn
        try:
            html_content = render_to_string('store/email/invoice.html', {
                'order': order,
                'cart_items': cart_items,
                'cart_total': cart_total
            })
            text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(
                f"Hóa đơn đặt hàng #{order.id} - Watch Store O2O",
                text_content,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@watchstore.com',
                [order.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
        except Exception as e:
            print("Lỗi khi gửi email:", e)
        
        # MÔ PHỎNG: Redirect sang Cổng VNPAY / MoMo thay vì Success
        return redirect('store:payment_create', order_id=order.id)

    return render(request, 'store/cart/checkout.html', {
        'cart_items': cart_items,
        'sub_total': cart_total,
        'discount_amount': discount_amount,
        'cart_total': final_total, # Tại checkout hiển thị Tổng cuối là chủ yếu
    })

def checkout_success(request):
    return render(request, 'store/cart/checkout_success.html')

# --- MÔ PHỎNG CỔNG THANH TOÁN (VNPAY / MOMO) ---
def payment_create(request, order_id):
    """
    Giả lập trang xử lý Hash Code trước khi nhảy sang cổng thanh toán.
    """
    order = get_object_or_404(Order, id=order_id)
    
    # Tại đây, hệ thống thực thụ sẽ chạy thư viện tạo vnp_HashMac
    # Ở đây ta sẽ giả lập UI Redirect.
    context = {
        'order': order,
        'vnp_return_url': f'/payment/return/?vnp_ResponseCode=00&vnp_TxnRef={order.id}'
    }
    return render(request, 'store/cart/payment_mock.html', context)

def payment_return(request):
    """
    Giả lập IPN / Return URL để hứng kết quả từ VNPAY.
    """
    vnp_ResponseCode = request.GET.get('vnp_ResponseCode')
    vnp_TxnRef = request.GET.get('vnp_TxnRef')
    
    if vnp_ResponseCode == '00':
        from store.models.order import Order
        order = get_object_or_404(Order, id=vnp_TxnRef)
        order.status = 'Processing' # Đã thanh toán
        order.save()
        
        return redirect('store:checkout_success')
        
    return redirect('store:cart_detail')