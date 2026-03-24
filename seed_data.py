import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import random
from store.models import Category, Product

# Clear existing simple data? Or just append. We'll just append, or check if exist.
categories_data = [
    {"name": "Rolex", "description": "Thương hiệu đồng hồ cao cấp từ Thuỵ Sĩ", "slug": "rolex"},
    {"name": "Omega", "description": "Thương hiệu đồng hồ danh tiếng với lịch sử ấn tượng", "slug": "omega"},
    {"name": "Seiko", "description": "Đồng hồ chất lượng cao từ Nhật Bản", "slug": "seiko"},
    {"name": "Casio", "description": "Đồng hồ điện tử bền bỉ và hiện đại", "slug": "casio"},
    {"name": "Tissot", "description": "Sự kết hợp hoàn hảo giữa truyền thống và đổi mới", "slug": "tissot"},
    {"name": "Orient", "description": "Đồng hồ cơ khí Nhật Bản với thiết kế cổ điển", "slug": "orient"}
]

products_data = {
    "Rolex": [
        {"name": "Rolex Submariner Date", "price": 350000000, "desc": "Mẫu đồng hồ lặn huyền thoại với thiết kế vượt thời gian."},
        {"name": "Rolex Daytona Cosmograph", "price": 850000000, "desc": "Đồng hồ bấm giờ thể thao được săn đón nhất."},
        {"name": "Rolex Datejust 41", "price": 280000000, "desc": "Biểu tượng của sự sang trọng cổ điển."}
    ],
    "Omega": [
        {"name": "Omega Speedmaster Moonwatch", "price": 180000000, "desc": "Chiếc đồng hồ đầu tiên lên mặt trăng."},
        {"name": "Omega Seamaster Diver 300M", "price": 140000000, "desc": "Sự lựa chọn của James Bond."},
        {"name": "Omega Aqua Terra 150M", "price": 150000000, "desc": "Thiết kế thanh lịch cho cả mặt đất và trên biển."}
    ],
    "Seiko": [
        {"name": "Seiko Prospex Alpinist", "price": 18500000, "desc": "Đồng hồ thám hiểm với thiết kế xanh lá cây đặc trưng."},
        {"name": "Seiko Presage Cocktail Time", "price": 12000000, "desc": "Mặt số tuyệt đẹp lấy cảm hứng từ các loại cocktail."},
        {"name": "Seiko 5 Sports Automatic", "price": 7500000, "desc": "Sự khởi đầu hoàn hảo cho thế giới đồng hồ cơ."}
    ],
    "Casio": [
        {"name": "Casio G-Shock DW5600", "price": 2500000, "desc": "Thiết kế vuông cổ điển, siêu bền bỉ."},
        {"name": "Casio Edifice Chronograph", "price": 4500000, "desc": "Đồng hồ kim thao tác mượt mà với kết nối smartphone."},
        {"name": "Casio Vintage A168", "price": 1200000, "desc": "Thiết kế hoài cổ sống lưng mọi ánh nhìn."}
    ],
    "Tissot": [
        {"name": "Tissot PRX Powermatic 80", "price": 18500000, "desc": "Phong cách retro thập niên 70 với cỗ máy 80 giờ trữ cót."},
        {"name": "Tissot Le Locle Automatic", "price": 16000000, "desc": "Thiết kế vô cùng cổ điển, vinh danh quê hương của Tissot."},
        {"name": "Tissot Seastar 1000", "price": 22000000, "desc": "Đồng hồ lặn mạnh mẽ và thời trang."}
    ],
    "Orient": [
        {"name": "Orient Bambino Version 2", "price": 5500000, "desc": "Đồng hồ dress watch cổ điển với mặt kính vòm cong."},
        {"name": "Orient Kamasu Diver", "price": 7500000, "desc": "Đồng hồ lặn giá hợp lý tốt nhất thị trường."},
        {"name": "Orient Star Classic", "price": 15000000, "desc": "Dòng sản phẩm cao cấp của Orient với kim báo năng lượng."}
    ]
}

def seed():
    print("Bắt đầu tạo dữ liệu đồng hồ...")
    
    # Tạo Category
    category_objs = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={
                "description": cat_data["description"],
                "slug": cat_data["slug"],
                "active": True
            }
        )
        if created:
            print(f"Created category: {cat.name}")
        category_objs[cat.name] = cat
        
    # Tạo Product
    count = 0
    for cat_name, product_list in products_data.items():
        category = category_objs.get(cat_name)
        if not category:
            continue
            
        for p_data in product_list:
            # Random specs
            specs = {
                "Kính": random.choice(["Sapphire", "Kính khoáng (Mineral)", "Hardlex", "Nhựa"]),
                "Máy": random.choice(["Automatic (Cơ tự động)", "Quartz (Pin)", "Solar (Năng lượng ánh sáng)"]),
                "Chống nước": random.choice(["3 ATM", "5 ATM", "10 ATM", "20 ATM", "30 ATM"]),
                "Đường kính mặt": f"{random.choice([38, 39, 40, 41, 42, 43, 44])} mm",
                "Chất liệu dây": random.choice(["Dây kim loại", "Dây da", "Dây cao su", "Dây vải tự nhiên"])
            }
            
            product, created = Product.objects.get_or_create(
                name=p_data["name"],
                defaults={
                    "category": category,
                    "price": p_data["price"],
                    "description": p_data["desc"],
                    "specs": specs
                }
            )
            if created:
                print(f"Created product: {product.name} ({product.price:,.0f} đ)")
                count += 1
                
    print(f"Hoàn thành! Đã tạo mới {count} sản phẩm.")

if __name__ == "__main__":
    seed()
