from django.db import models
from django_json_widget.widgets import JSONEditorWidget

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

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
