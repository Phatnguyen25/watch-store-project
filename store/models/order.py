from django.db import models
from django.contrib.auth.models import User
from .product import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Chờ xử lý'),
        ('Processing', 'Đang xử lý'),
        ('Shipped', 'Đang giao hàng'),
        ('Delivered', 'Đã nhận hàng'),
        ('Cancelled', 'Đã hủy'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=150, blank=True, null=True, verbose_name="Email")
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"
