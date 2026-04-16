from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models.order import Order
from django.contrib.auth import update_session_auth_hash

@login_required(login_url='store:login')
def profile_view(request):
    user = request.user
    
    if request.method == 'POST':
        # Check if form is password change or info update
        old_password = request.POST.get('old_password')
        if old_password is not None:
            # Handle password change
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if not user.check_password(old_password):
                messages.error(request, "Mật khẩu cũ không chính xác!")
            elif new_password != confirm_password:
                messages.error(request, "Mật khẩu xác nhận không khớp!")
            elif len(new_password) < 6:
                messages.error(request, "Mật khẩu mới phải có ít nhất 6 ký tự.")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, "Đổi mật khẩu thành công!")
            return redirect('store:profile')
        else:
            # Update user basic info
            username = request.POST.get('username')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            
            # Username handling
            if username and username != user.username:
                from django.contrib.auth.models import User
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Tên đăng nhập này đã có người sử dụng.")
                    return redirect('store:profile')
                user.username = username
                
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, "Cập nhật Thông tin Cá nhân thành công!")
            return redirect('store:profile')
        
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'store/auth/profile.html', context)
