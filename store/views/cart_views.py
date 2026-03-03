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
    return redirect('cart_detail')

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
        
    return redirect('cart_detail')

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
        
    return redirect('cart_detail')
@login_required(login_url='/admin/login/')
def checkout(request):
    # 1. Lấy các sản phẩm đang có trong giỏ hàng của người dùng
    cart_items = CartItem.objects.filter(user=request.user)
    
    # 2. Nếu giỏ hàng trống, không cho thanh toán mà quay về trang sản phẩm
    if not cart_items.exists():
        return redirect('store:product_list')
        
    # 3. Tính tổng tiền cần thanh toán
    total_price = sum(item.total_price for item in cart_items)
    
    # 4. Trả về giao diện trang checkout.html cùng dữ liệu
    return render(request, 'store/cart/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
@login_required(login_url='/admin/login/')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('store:product_list')
        
    total_price = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        # Lấy thông tin khách hàng điền từ Form
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        notes = request.POST.get('notes')
        payment_method = request.POST.get('payment_method')

        # --- ĐOẠN NÀY LÀ ĐỂ LƯU VÀO DATABASE ---
        # Sau khi bạn tạo Model Order, chúng ta sẽ viết lệnh lưu ở đây
        
        # Xóa sạch giỏ hàng sau khi đặt thành công
        cart_items.delete()

        # Chuyển hướng sang trang thông báo thành công
        return render(request, 'store/cart/order_success.html')

    return render(request, 'store/cart/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })