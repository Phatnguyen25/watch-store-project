import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Product, Order, OrderItem

def seed():
    print("Bắt đầu tạo tài khoản và đơn hàng giả lập...")

    # 1. Tạo 1 tài khoản Admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@watchstore.com', 'adminpass123')
        print("Đã tạo tài khoản Admin: admin / adminpass123")
    else:
        admin = User.objects.get(username='admin')
        print("Tài khoản Admin đã tồn tại.")

    # 2. Tạo 2 tài khoản User
    users = []
    for i in range(1, 3):
        username = f'user{i}'
        email = f'user{i}@example.com'
        password = 'userpass123'
        if not User.objects.filter(username=username).exists():
            u = User.objects.create_user(username, email, password)
            print(f"Đã tạo tài khoản: {username} / {password}")
            users.append(u)
        else:
            u = User.objects.get(username=username)
            users.append(u)

    # 3. Tạo 100 đơn hàng
    products = list(Product.objects.all())
    if not products:
        print("Không có sản phẩm nào trong DB để tạo đơn. Hãy chạy seed_data.py trước.")
        return

    statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
    
    addresses = [
        "123 Nguyễn Văn Linh, Đà Nẵng",
        "45 Lê Duẩn, Hà Nội",
        "88 Tôn Đức Thắng, TP.HCM",
        "92 Hùng Vương, Cần Thơ",
        "15 Hai Bà Trưng, Hội An"
    ]

    orders_created = 0
    for i in range(100):
        # Chọn ngẫu nhiên 1 trong 2 user
        u = random.choice(users)
        
        # Tạo Order
        order = Order.objects.create(
            user=u,
            email=u.email,
            full_name=f"Khách hàng {u.username.capitalize()}",
            phone=f"09{random.randint(10000000, 99999999)}",
            address=random.choice(addresses),
            status=random.choice(statuses)
        )
        
        # Lùi ngày tạo đơn hàng ngẫu nhiên trong 30 ngày qua
        random_days_ago = random.randint(0, 30)
        order.created_at = timezone.now() - timedelta(days=random_days_ago)
        
        # Chọn ngẫu nhiên 1-3 sản phẩm
        num_items = random.randint(1, 3)
        selected_products = random.sample(products, num_items)
        
        total_price = 0
        for p in selected_products:
            qty = random.randint(1, 2)
            price = p.price
            OrderItem.objects.create(
                order=order,
                product=p,
                price=price,
                quantity=qty
            )
            total_price += price * qty
            
        order.total_price = total_price
        order.save()
        orders_created += 1

    print(f"Hoàn thành! Đã tạo thành công {orders_created} đơn hàng.")

if __name__ == "__main__":
    seed()
