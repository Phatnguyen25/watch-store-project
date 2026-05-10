from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã giảm giá")
    discount_percent = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="Phần trăm giảm (%)"
    )
    active = models.BooleanField(default=True, verbose_name="Còn hiệu lực")
    valid_to = models.DateTimeField(verbose_name="Hạn sử dụng", null=True, blank=True)
    
    def __str__(self):
        return f"{self.code} (-{self.discount_percent}%)"