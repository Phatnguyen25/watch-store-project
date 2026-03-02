# store/forms.py
from django import forms
from .models import Product

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
            
            # Ô nhập JSON (Tạm thời dùng Textarea, người dùng sẽ tự gõ JSON tay)
            'specs': forms.Textarea(attrs={
                'class': 'w-full mt-1 font-mono text-sm rounded-md border-gray-300 shadow-sm focus:border-blue-500', 
                'rows': 3,
                'placeholder': '{"movement": "Automatic", "glass": "Sapphire", "water_proof": "5ATM"}'
            }),
        }