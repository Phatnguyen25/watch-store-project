import os
import django
import random

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Product, ProductReview
from django.contrib.auth.models import User

def seed_reviews():
    products = Product.objects.all()
    users = list(User.objects.filter(is_staff=False)[:10])
    
    if not users:
        print("Không tìm thấy người dùng thường để tạo đánh giá mẫu.")
        return

    reviews_pool = [
        "Sản phẩm tuyệt vời, rất đáng đồng tiền bát gạo!",
        "Thiết kế sang trọng, đeo rất êm tay.",
        "Giao hàng nhanh, đóng gói cẩn thận. Rất ưng ý.",
        "Đồng hồ đẹp hơn cả trong ảnh, 5 sao!",
        "Chất lượng hoàn thiện tốt, mặt kính sáng bóng.",
        "Mua tặng chồng mà chồng khen suốt. Cảm ơn shop.",
        "Sẽ ủng hộ shop dài dài, phục vụ quá nhiệt tình.",
        "Hàng chính hãng, check code thoải mái.",
        "Màu sắc rất bắt mắt, phối đồ cực dễ.",
        "Dây đeo chắc chắn, cảm giác rất cao cấp."
    ]

    count = 0
    for product in products:
        # Chọn ngẫu nhiên 1-2 bình luận cho mỗi sản phẩm
        num_reviews = random.randint(1, 2)
        random.shuffle(users)
        
        for i in range(min(num_reviews, len(users))):
            user = users[i]
            
            # Kiểm tra xem user này đã đánh giá chưa để tránh trùng lặp
            if not ProductReview.objects.filter(product=product, user=user).exists():
                ProductReview.objects.create(
                    product=product,
                    user=user,
                    rating=random.choice([4, 5]), # Chỉ seed đánh giá tốt
                    content=random.choice(reviews_pool)
                )
                count += 1
    
    print(f"Đã tạo thành công {count} đánh giá mẫu cho {products.count()} sản phẩm.")

if __name__ == "__main__":
    seed_reviews()
