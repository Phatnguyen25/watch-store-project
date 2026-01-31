from django.db import models
from django.contrib.gis.db import models as gis_models # Thư viện xử lý bản đồ

# 1. Danh mục đồng hồ (Nam/Nữ/Cơ/Điện tử...)
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# 2. Sản phẩm Đồng hồ (Sử dụng JSONField cho thông số kỹ thuật)
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=0) # Giá VND
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # SỨC MẠNH CỦA JSON: Lưu trữ linh hoạt (Máy, Kính, Chống nước...)
    # Ví dụ: {"movement": "Automatic", "glass": "Sapphire", "water_proof": "5ATM"}
    specs = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return self.name

# 3. Cửa hàng (Sử dụng PostGIS để lưu tọa độ)
class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    
    # PointField: Lưu Kinh độ (Longitude) và Vĩ độ (Latitude)
    location = gis_models.PointField(srid=4326) 
    
    def __str__(self):
        return self.name