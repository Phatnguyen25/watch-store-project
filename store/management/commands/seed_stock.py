import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Product, StockHistory

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho lịch sử kho'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        user = User.objects.filter(is_superuser=True).first()
        
        if not products.exists():
            self.stdout.write(self.style.ERROR('Chưa có sản phẩm nào. Vui lòng thêm sản phẩm trước.'))
            return

        if not user:
            user = User.objects.first()

        types = ['Import', 'Update', 'Sale', 'Return']
        notes = [
            'Nhập hàng định kỳ tháng 4',
            'Kiểm kê cuối ngày',
            'Bán lẻ cho khách tại quầy',
            'Hoàn trả hàng lỗi',
            'Điều chỉnh stock sau khi đếm lại'
        ]

        count = 0
        for product in products:
            # Tạo ngẫu nhiên 2-5 bản ghi lịch sử cho mỗi sản phẩm
            for _ in range(random.randint(2, 5)):
                stock_before = product.stock
                change = random.randint(-10, 20)
                
                # Tránh stock âm quá nhiều
                if stock_before + change < 0:
                    change = -stock_before
                
                stock_after = stock_before + change
                h_type = random.choice(types)
                
                StockHistory.objects.create(
                    product=product,
                    user=user,
                    stock_before=stock_before,
                    stock_after=stock_after,
                    change_amount=change,
                    type=h_type,
                    note=random.choice(notes)
                )
                
                # Cập nhật luôn stock của sản phẩm để dữ liệu trông thật hơn
                product.stock = stock_after
                product.save()
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Đã tạo thành công {count} bản ghi lịch sử kho mẫu.'))
