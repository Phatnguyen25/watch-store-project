from django.db import models
from django.contrib.auth.models import User
from .product import Product

class StockHistory(models.Model):
    TYPE_CHOICES = (
        ('Import', 'Nhập hàng (Excel)'),
        ('Update', 'Cập nhật thủ công'),
        ('Sale', 'Bán hàng'),
        ('Return', 'Hoàn hàng'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    stock_before = models.IntegerField(default=0)
    stock_after = models.IntegerField(default=0)
    change_amount = models.IntegerField(default=0)
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Update')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lịch sử kho"
        verbose_name_plural = "Lịch sử kho"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.change_amount} ({self.type})"
