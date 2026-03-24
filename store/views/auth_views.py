from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django import forms

# Tùy chỉnh form đăng ký để yêu cầu nhập email
class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Địa chỉ Email")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')
        
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Đăng ký thành công! Chào mừng {user.username}.")
            next_url = request.GET.get('next')
            if not next_url:
                next_url = 'store:product_list'
            return redirect(next_url)
    else:
        form = CustomRegisterForm()
        
    return render(request, 'store/auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next')
            if not next_url:
                next_url = 'store:product_list'
            return redirect(next_url)
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
    else:
        form = AuthenticationForm()

    return render(request, 'store/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Bạn đã đăng xuất thành công.")
    return redirect('store:product_list')
