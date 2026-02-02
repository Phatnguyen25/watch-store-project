from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product, CartItem

# 1. Chức năng Thêm vào giỏ
@login_required(login_url='/admin/login/')  # Bắt buộc đăng nhập mới được mua
def add_to_cart(request, product_id):
    # Lấy sản phẩm theo ID, nếu không có thì báo lỗi 404
    product = get_object_or_404(Product, id=product_id)
    
    # Tìm xem trong giỏ của user này đã có sản phẩm đó chưa
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    # Nếu đã có rồi thì tăng số lượng lên 1
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Mua xong thì quay lại trang danh sách (tạm thời)
    return redirect('store:product_list')

# 2. Chức năng Xem giỏ hàng
@login_required(login_url='/admin/login/')
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    
    return render(request, 'store/cart/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
# 3. Hàm Xóa sản phẩm khỏi giỏ
@login_required(login_url='/admin/login/')
def remove_from_cart(request, item_id):
    # Tìm sản phẩm trong giỏ để xóa
    cart_item = CartItem.objects.filter(id=item_id, user=request.user).first()
    if cart_item:
        cart_item.delete()
    return redirect('store:cart_detail')

# 4. Hàm Tăng/Giảm số lượng
@login_required(login_url='/admin/login/')
def update_cart(request, item_id, action):
    cart_item = CartItem.objects.filter(id=item_id, user=request.user).first()
    
    if cart_item:
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1
        
        # Nếu giảm xuống 0 hoặc ít hơn thì xóa luôn
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
            
    return redirect('store:cart_detail')