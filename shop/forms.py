from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'original_price', 
                  'subtitle', 'description', 'image', 'video', 'rating', 
                  'badge_text', 'is_new', 'is_bestseller', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full h-12 bg-stone-50 border border-stone-100 rounded-xl px-4 text-sm font-bold text-luxe-navy focus:border-luxe-gold focus:ring-0 outline-none'}),
            'category': forms.Select(attrs={'class': 'luxe-select w-full h-12 bg-stone-50 border border-stone-100 rounded-xl px-4 text-sm font-bold text-luxe-navy focus:border-luxe-gold focus:ring-0 outline-none'}),
            'subtitle': forms.TextInput(attrs={'class': 'w-full h-12 bg-stone-50 border border-stone-100 rounded-xl px-4 text-sm font-bold text-luxe-navy focus:border-luxe-gold focus:ring-0 outline-none'}),
            'price': forms.NumberInput(attrs={'class': 'w-full h-12 bg-stone-50 border border-stone-100 rounded-xl px-4 text-sm font-bold text-luxe-navy focus:border-luxe-gold focus:ring-0 outline-none'}),
            'original_price': forms.NumberInput(attrs={'class': 'w-full h-12 bg-stone-50 border border-stone-100 rounded-xl px-4 text-sm font-bold text-luxe-navy focus:border-luxe-gold focus:ring-0 outline-none'}),
            'rating': forms.NumberInput(attrs={'class': 'w-full h-12 bg-stone-50 border border-stone-100 rounded-xl px-4 text-sm font-bold text-luxe-navy focus:border-luxe-gold focus:ring-0 outline-none', 'step': '0.1'}),
            'badge_text': forms.TextInput(attrs={'class': 'w-full h-12 bg-stone-50 border border-stone-100 rounded-xl px-4 text-sm font-bold text-luxe-navy focus:border-luxe-gold focus:ring-0 outline-none'}),
            'description': forms.Textarea(attrs={'class': 'w-full h-32 bg-stone-50 border border-stone-100 rounded-xl p-4 text-sm font-medium text-luxe-navy focus:border-luxe-gold focus:ring-0 outline-none'}),
            'is_new': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-luxe-navy border-stone-300 rounded focus:ring-luxe-gold'}),
            'is_bestseller': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-luxe-navy border-stone-300 rounded focus:ring-luxe-gold'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-luxe-navy border-stone-300 rounded focus:ring-luxe-gold'}),
        }
