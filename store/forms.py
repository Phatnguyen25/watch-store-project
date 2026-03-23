from django import forms
from .models import Product, Store, Category, Coupon
from .models.order import Order
from leaflet.forms.widgets import LeafletWidget

# ==========================================
# 1. FORM CỬA HÀNG (Do bạn custom)
# ==========================================
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-blue-500'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-blue-500'}),
            'location': LeafletWidget(attrs={'map_width': '100%', 'map_height': '300px'})
        }

# ==========================================
# 2. FORM SẢN PHẨM (Do bạn custom)
# ==========================================
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'description', 'image', 'specs']
        
        # Nhúng class Tailwind vào các thẻ input của HTML
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'name': forms.TextInput(attrs={'class': 'w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'price': forms.NumberInput(attrs={'class': 'w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'w-full mt-1 text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),
            
            # Ô nhập JSON
            'specs': forms.Textarea(attrs={
                'class': 'w-full mt-1 font-mono text-sm rounded-md border-gray-300 shadow-sm focus:border-blue-500', 
                'rows': 3,
                'placeholder': '{"movement": "Automatic", "glass": "Sapphire", "water_proof": "5ATM"}'
            }),
        }

# ==========================================
# 3. FORM DANH MỤC (MỚI THÊM)
# ==========================================
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-blue-500'}),
            'slug': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-blue-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-blue-500', 'rows': 3}),
            'active': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer mt-2'}),
        }

# ==========================================
# 4. FORM MÃ GIẢM GIÁ (MỚI THÊM)
# ==========================================
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'
        widgets = {
            'code': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-blue-500 uppercase', 'placeholder': 'VD: FREESHIP'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-blue-500', 'placeholder': '10'}),
            'active': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer mt-2'}),
        }

# ==========================================
# 5. FORM ĐƠN HÀNG
# ==========================================
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'w-full mt-1 px-4 py-2 border rounded-lg focus:ring-blue-500'}),
        }