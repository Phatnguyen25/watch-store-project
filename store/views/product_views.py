from django.shortcuts import render
# Tạm thời comment các model lại vì chúng ta chưa cần gọi Database
# from store.models import Product, Category 

def product_list(request):
    """VIEW TĨNH: Trang danh sách sản phẩm"""
    
    mock_products = [
        {
            'pk': 1, # Dùng pk thay cho id để khớp với url của bạn
            'name': 'Rolex Submariner Date', 
            'price': '350.000.000', 
            'category': 'Đồng hồ cơ',
            'image': 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=500&q=80'
        },
        {
            'pk': 2, 
            'name': 'Omega Speedmaster', 
            'price': '180.000.000', 
            'category': 'Đồng hồ cơ',
            'image': 'https://images.unsplash.com/photo-1548171915-e76a3e1eb520?auto=format&fit=crop&w=500&q=80'
        },
        {
            'pk': 3, 
            'name': 'Casio G-Shock', 
            'price': '4.500.000', 
            'category': 'Đồng hồ điện tử',
            'image': 'https://images.unsplash.com/photo-1517502884422-41eaead166d4?auto=format&fit=crop&w=500&q=80'
        }
    ]
    
    return render(request, 'store/product/list.html', {'products': mock_products})

def product_detail(request, pk):
    """VIEW TĨNH: Trang chi tiết 1 sản phẩm"""
    
    # Tạo 1 dữ liệu giả lập duy nhất. 
    # Bất kể bạn gõ ID số mấy trên URL, nó cũng sẽ in ra cái đồng hồ này.
    mock_product = {
        'pk': pk,
        'name': f'Đồng Hồ Mẫu (Mã số {pk})',
        'price': '12.500.000',
        'category': 'Đồng hồ cơ',
        'description': 'Đây là đoạn mô tả mẫu để bạn thiết kế giao diện. Đồng hồ thiết kế sang trọng, bộ máy cơ tự động, mặt kính Sapphire nguyên khối chống xước hoàn hảo.',
        'image': 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=800&q=80',
        'specs': {
            'Thương hiệu': 'Rolex',
            'Bộ máy': 'Automatic (Cơ tự động)',
            'Mặt kính': 'Sapphire',
            'Chống nước': '10 ATM'
        }
    }
    
    return render(request, 'store/product/details.html', {'product': mock_product})