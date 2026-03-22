from django.db import models
from .category import Category

class Product(models.Model):
    # Thay đổi CASCADE thành SET_NULL để bảo vệ dữ liệu sản phẩm
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='products',
        verbose_name="Danh mục"
    )
    
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá (VNĐ)")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Hình ảnh")
    
    # SỨC MẠNH CỦA JSON: Lưu trữ linh hoạt (Máy, Kính, Chống nước...)
    specs = models.JSONField(default=dict, blank=True, verbose_name="Thông số kỹ thuật")
    
    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Các sản phẩm"

    def __str__(self):
        return self.name