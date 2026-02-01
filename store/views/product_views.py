from django.shortcuts import render, get_object_or_404
from store.models import Product, Category # Import vẫn giữ nguyên nhờ bước 1

def product_list(request):
    products = Product.objects.all()
    # Đường dẫn này dựa trên cấu trúc folder: store/templates/store/product_list.html
    return render(request, 'store/product/list.html', {'products': products})
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # LƯU Ý: Tên file ở đây phải khớp với file bạn tạo trong hình (details_product.html)
    return render(request, 'store/product/details.html', {'product': product})