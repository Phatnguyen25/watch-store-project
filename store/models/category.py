from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name="Đường dẫn (Slug)")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    active = models.BooleanField(default=True, verbose_name="Hiển thị")

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Các danh mục"

    def __str__(self):
        return self.name