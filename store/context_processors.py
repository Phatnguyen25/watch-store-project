def cart_count(request):
    """Đếm tổng số lượng đồng hồ đang có trong Giỏ hàng (Session)"""
    cart = request.session.get('cart', {})
    total_items = sum(cart.values()) # Cộng dồn tất cả số lượng lại
    return {'cart_count': total_items}