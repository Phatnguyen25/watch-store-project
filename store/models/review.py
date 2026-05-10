from django.db import models
from django.contrib.auth.models import User
from .product import Product

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Sản phẩm")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    rating = models.IntegerField(default=5, verbose_name="Đánh giá (sao)")
    content = models.TextField(verbose_name="Nội dung bình luận")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Đánh giá sản phẩm"
        verbose_name_plural = "Các đánh giá sản phẩm"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"
