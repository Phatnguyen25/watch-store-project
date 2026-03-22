from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from store.models import Product, Coupon
from django.contrib.humanize.templatetags.humanize import intcomma

def get_cart_data(request):
    """Hàm bổ trợ: Tính toán dữ liệu giỏ hàng từ Session"""
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    for product_id_str, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id_str))
            total_price = product.price * quantity
            cart_total += total_price
            
            cart_items.append({
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
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('store:cart_detail')

def cart_detail(request):
    cart_items, cart_total = get_cart_data(request)
    return render(request, 'store/cart/cart_detail.html', {
        'cart_items': cart_items, 
        'cart_total': cart_total
    })

def update_cart(request, item_id, action):
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

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:product_list')

    if request.method == 'POST':
        # Sau này Tech Lead viết logic tạo Order vào DB ở đây nhé
        request.session['cart'] = {}
        request.session.modified = True
        return redirect('store:checkout_success')

    cart_items, cart_total = get_cart_data(request)
    return render(request, 'store/cart/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })

def checkout_success(request):
    return render(request, 'store/cart/checkout_success.html')