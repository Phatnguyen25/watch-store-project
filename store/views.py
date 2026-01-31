from django.shortcuts import render
from .models import Product # Gọi Model (M)

# Đây là Controller
def product_list(request):
    # 1. Gọi Model để lấy toàn bộ sản phẩm
    products = Product.objects.all()
    
    # 2. Chuẩn bị dữ liệu để gửi sang View
    context = {
        'products': products
    }
    
    # 3. Trả về giao diện (View) kèm dữ liệu
    return render(request, 'store/product_list.html', context)