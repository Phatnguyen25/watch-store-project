from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from store.models.cart import CartItem # Hoặc đường dẫn chính xác đến file chứa CartItem của bạn
def add_to_cart(request, product_id):
    """Thêm sản phẩm vào giỏ hàng Session"""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    return redirect('store:cart_detail')

def cart_detail(request):
    """Lấy dữ liệu thật từ DB và tính tiền"""
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    # Lặp qua từng ID sản phẩm trong Session
    for product_id_str, quantity in cart.items():
        try:
            # Truy vấn DB để lấy giá và tên thật
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
            pass # Lỡ sản phẩm bị Admin xóa thì bỏ qua

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total
    }
    return render(request, 'store/cart/cart_detail.html', context)

def remove_from_cart(request, item_id):
    """Xóa hẳn 1 món khỏi giỏ hàng"""
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        del cart[item_id_str]
        request.session['cart'] = cart
        
    return redirect('store:cart_detail')

def update_cart(request, item_id, action):
    """Tăng (+) hoặc Giảm (-) số lượng"""
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        if action == 'increase':
            cart[item_id_str] += 1
        elif action == 'decrease':
            cart[item_id_str] -= 1
            # Nếu giảm xuống 0 thì xóa luôn khỏi giỏ
            if cart[item_id_str] <= 0:
                del cart[item_id_str]
                
        request.session['cart'] = cart
        
    return redirect('store:cart_detail')

def checkout(request):
    """Xử lý thanh toán"""
    # 1. Lấy giỏ hàng từ session
    cart = request.session.get('cart', {})
    
    # Nếu giỏ trống thì quay về trang sản phẩm
    if not cart:
        return redirect('store:product_list')

    # 2. Xử lý khi khách bấm nút "Xác nhận Đặt hàng" (Method POST)
    if request.method == 'POST':
        # Tạm thời làm sạch giỏ hàng
        request.session['cart'] = {}
        request.session.modified = True
        return redirect('store:checkout_success')

    # 3. Truy vấn Database để tính toán giỏ hàng khi hiển thị trang
    cart_items = []
    cart_total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            total = product.price * quantity
            cart_total += total
            
            item_data = {
                'product_id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'total': total,
            }
            
            if product.image:
                item_data['image'] = product.image.url
                
            cart_items.append(item_data)
            
        except Product.DoesNotExist:
            pass

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    # DÒNG NÀY RẤT QUAN TRỌNG ĐỂ TRÁNH LỖI VIEW TRẢ VỀ NONE
    return render(request, 'store/cart/checkout.html', context)

def checkout_success(request):
    """Trang thông báo đặt hàng thành công"""
    return render(request, 'store/cart/checkout_success.html')