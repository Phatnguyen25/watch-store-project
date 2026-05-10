import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Coupon

def run():
    print("Bắt đầu tạo 10 mã giảm giá...")
    
    coupons_data = [
        {"code": "WELCOME10", "discount": 10},
        {"code": "SUMMER20", "discount": 20},
        {"code": "VIP50", "discount": 50},
        {"code": "FREESHIP", "discount": 5},
        {"code": "FLASH15", "discount": 15},
        {"code": "MEGA30", "discount": 30},
        {"code": "O2OSPECIAL", "discount": 25},
        {"code": "NEWYEAR2026", "discount": 40},
        {"code": "LUCKY88", "discount": 8},
        {"code": "CRAZYDEAL", "discount": 60},
    ]
    
    count = 0
    for data in coupons_data:
        # Hạn sử dụng random từ 10 đến 30 ngày tới
        valid_until = timezone.now() + timedelta(days=random.randint(10, 30))
        
        coupon, created = Coupon.objects.get_or_create(
            code=data["code"],
            defaults={
                'discount_percent': data["discount"],
                'active': True,
                'valid_to': valid_until
            }
        )
        if created:
            print(f"✅ Đã tạo mã: {coupon.code} (Giảm {coupon.discount_percent}%) - Hạn: {coupon.valid_to.strftime('%d/%m/%Y')}")
            count += 1
        else:
            print(f"⚠️ Mã {coupon.code} đã tồn tại.")
            
    print(f"\n🎉 Hoàn tất! Đã thêm mới {count} mã giảm giá.")

if __name__ == '__main__':
    run()
