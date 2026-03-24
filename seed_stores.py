import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Store
from django.contrib.gis.geos import Point

def seed():
    print("Bắt đầu tạo 20 cửa hàng giả lập...")
    
    # Xoá các cửa hàng cũ nếu muốn (ở đây mình giữ nguyên và thêm mới)
    # Store.objects.all().delete()
    
    # Tạo dữ liệu mẫu
    cities = [
        ("Hà Nội", 105.8542, 21.0285),
        ("Hồ Chí Minh", 106.6297, 10.8231),
        ("Đà Nẵng", 108.2022, 16.0544),
        ("Hải Phòng", 106.6881, 20.8449),
        ("Cần Thơ", 105.7706, 10.0452),
        ("Nha Trang", 109.1967, 12.2388),
        ("Huế", 107.5905, 16.4637),
        ("Đà Lạt", 108.4383, 11.9404)
    ]
    
    store_names = ["WatchStore Center", "WatchStore Premium", "WatchStore Standard", "WatchStore Express", "WatchStore Outlet"]
    street_names = ["Lê Duẩn", "Nguyễn Văn Linh", "Trần Hưng Đạo", "Hai Bà Trưng", "Lê Lợi", "Nguyễn Trãi", "Phan Đình Phùng", "Quang Trung"]
    
    count = 0
    for i in range(20):
        # Chọn ngẫu nhiên một thành phố
        city_name, base_lon, base_lat = random.choice(cities)
        
        # Thêm sai số nhỏ để tạo tọa độ ngẫu nhiên xung quanh thành phố
        lat = base_lat + random.uniform(-0.05, 0.05)
        lon = base_lon + random.uniform(-0.05, 0.05)
        
        name = f"{random.choice(store_names)} {city_name} #{i+1}"
        address = f"Số {random.randint(1, 999)} {random.choice(street_names), city_name}"
        phone = f"09{random.randint(10000000, 99999999)}"
        
        # Tạo object Point (Lưu ý thứ tự: Longitude trước, Latitude sau)
        location = Point(lon, lat, srid=4326)
        
        Store.objects.create(
            name=name,
            address=address,
            phone=phone,
            location=location
        )
        count += 1
        print(f"[{count}] Tạo cửa hàng: {name} ở {city_name} (Tọa độ: {lat:.4f}, {lon:.4f})")
        
    print(f"Đã tạo thành công {count} cửa hàng!")

if __name__ == "__main__":
    seed()
