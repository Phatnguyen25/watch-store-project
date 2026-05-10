import os
import django
import random
import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Order, OrderItem, Product
from django.contrib.auth.models import User

def seed_data():
    products = list(Product.objects.all())
    if not products:
        print("Không có sản phẩm nào để tạo đơn hàng. Vui lòng thêm sản phẩm trước.")
        return

    # Lấy tài khoản admin hoặc user đầu tiên
    user = User.objects.first()
    
    # Xóa toàn bộ đơn hàng hiện có để làm mới hoàn toàn
    Order.objects.all().delete()
    print("Đã xóa các đơn hàng cũ.")

    statuses = ['Processing', 'Shipped', 'Delivered', 'Delivered', 'Delivered', 'Cancelled']
    names = ['Nguyễn Văn A', 'Trần Thị B', 'Lê Văn C', 'Phạm Minh D', 'Hoàng Anh E', 'Đặng Thu F', 'Vũ Văn G', 'Bùi Thị H', 'Nguyễn Thị I', 'Trần Văn K']
    addresses = ['Hà Nội', 'TP. HCM', 'Đà Nẵng', 'Cần Thơ', 'Hải Phòng', 'Bình Dương', 'Quảng Ninh', 'Huế', 'Đồng Nai']

    now = datetime.datetime.now()
    year = now.year
    
    start_date = datetime.date(year, 1, 1)
    end_date = now.date()
    
    delta = end_date - start_date
    days = delta.days + 1

    total_created = 0

    print(f"Bắt đầu seed dữ liệu từ đầu năm {year} đến hiện tại ({end_date.strftime('%d/%m/%Y')})...")

    # Tạo dữ liệu từ ngày 1/1 đến ngày hôm nay
    for i in range(days):
        current_date = start_date + datetime.timedelta(days=i)
        
        # Mỗi ngày tạo từ 1 đến 5 đơn hàng để biểu đồ có biến động
        num_orders = random.randint(1, 5)
        for _ in range(num_orders):
            # Tạo thời gian ngẫu nhiên trong ngày
            hour = random.randint(8, 20)
            minute = random.randint(0, 59)
            
            created_at = timezone.make_aware(
                datetime.datetime.combine(current_date, datetime.time(hour, minute))
            )

            # Tạo Order
            order = Order.objects.create(
                user=user,
                full_name=random.choice(names),
                email=f"customer{total_created}@example.com",
                phone=f"09{random.randint(10000000, 99999999)}",
                address=random.choice(addresses),
                status=random.choice(statuses),
                total_price=0
            )

            # Cập nhật created_at vì auto_now_add có thể ghi đè
            Order.objects.filter(id=order.id).update(created_at=created_at)

            # Tạo từ 1 đến 3 OrderItem
            num_items = random.randint(1, 3)
            order_total = 0
            selected_products = random.sample(products, min(num_items, len(products)))
            
            for product in selected_products:
                qty = random.randint(1, 2)
                price = product.price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=price,
                    quantity=qty
                )
                order_total += (price * qty)

            # Cập nhật tổng tiền đơn hàng
            Order.objects.filter(id=order.id).update(total_price=order_total)
            
            total_created += 1

    print(f"Hoàn thành! Đã tạo thành công {total_created} đơn hàng mẫu.")

if __name__ == "__main__":
    seed_data()
