from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg
from store.models import Product, Category, ProductReview
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def product_list(request):
    """Trang danh mục sản phẩm kết hợp Live-Search"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True).order_by('-id')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    # Nếu là yêu cầu AJAX (thường từ Live Search)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/product/product_grid_fragment.html', {'products': products})

    best_sellers = Product.objects.filter(is_active=True).order_by('stock')[:4]
    categories = Category.objects.filter(active=True)
    
    return render(request, 'store/product/list.html', {
        'products': products,
        'best_sellers': best_sellers,
        'categories': categories,
        'query': query
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
        
    # Phân trang, mỗi trang 10 sản phẩm
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
        
    return render(request, 'store/product/all_products.html', {
        'products': page_products,
        'categories': categories,
        'query': query,
        'category_id': category_id,
    })

def product_detail(request, pk):
    """Trang chi tiết 1 sản phẩm (lấy từ Database)"""
    product = get_object_or_404(Product, pk=pk)
    # Lấy danh sách đánh giá mới nhất
    reviews = product.reviews.all().select_related('user').order_by('-created_at')
    # Tính điểm trung bình
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 5.0
    
    # Lấy đánh giá của chính user hiện tại (nếu có)
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    return render(request, 'store/product/details.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'reviews_count': reviews.count(),
        'user_review': user_review
    })

@login_required
def add_product_review(request, product_id):
    """Xử lý thêm hoặc Cập nhật đánh giá qua AJAX"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = request.POST.get('rating', 5)
        content = request.POST.get('content', '')

        if not content:
            return JsonResponse({'status': 'error', 'message': 'Vui lòng nhập nội dung bình luận.'}, status=400)

        # Sử dụng update_or_create để cho phép người dùng chỉnh sửa đánh giá cũ
        review, created = ProductReview.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                'rating': int(rating),
                'content': content
            }
        )

        return JsonResponse({
            'status': 'success',
            'is_update': not created,
            'message': 'Cập nhật thành công!' if not created else 'Gửi đánh giá thành công!',
            'user': review.user.username,
            'rating': review.rating,
            'content': review.content,
            'created_at': review.created_at.strftime('%d/%m/%Y %H:%M')
        })
    
    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ.'}, status=400)