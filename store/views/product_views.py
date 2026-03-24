from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from store.models import Product, Category

def product_list(request):
    """Trang danh sách sản phẩm (lấy từ Database)"""
    products = Product.objects.filter(is_active=True).order_by('-id')
    categories = Category.objects.filter(active=True)
    return render(request, 'store/product/list.html', {
        'products': products,
        'categories': categories
    })

def category_products(request, slug):
    """Trang danh sách sản phẩm theo danh mục"""
    category = get_object_or_404(Category, slug=slug, active=True)
    products = Product.objects.filter(category=category, is_active=True).order_by('-id')
    categories = Category.objects.filter(active=True)
    
    return render(request, 'store/product/category_products.html', {
        'category': category,
        'products': products,
        'categories': categories
    })

def all_products(request):
    """Trang danh sách MỌI sản phẩm"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category_id', '')
    
    products = Product.objects.filter(is_active=True).order_by('-id')
    categories = Category.objects.filter(active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
    if category_id:
        products = products.filter(category_id=category_id)
        
    return render(request, 'store/product/all_products.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'category_id': category_id,
    })

def product_detail(request, pk):
    """Trang chi tiết 1 sản phẩm (lấy từ Database)"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product/details.html', {'product': product})