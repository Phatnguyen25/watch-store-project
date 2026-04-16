from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django import forms

def sync_session_cart_to_db(request, user):
    from store.models import CartItem, Product
    session_cart = request.session.get('cart', {})
    if not session_cart:
        return
        
    for product_id_str, quantity in session_cart.items():
        try:
            product = Product.objects.get(id=int(product_id_str))
            cart_item, created = CartItem.objects.get_or_create(
                user=user,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        except Product.DoesNotExist:
            continue
            
    # Giữ an toàn bằng cách làm sạch session
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True

# Tùy chỉnh form đăng ký để yêu cầu nhập email
class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Địa chỉ Email")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

def register_view(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')
        
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Tài khoản tạm thời bị khóa chờ email
            user.save()
            
            # Bắn Email xác thực
            current_site = get_current_site(request)
            mail_subject = 'Kích hoạt tài khoản Watch Store O2O'
            message = render_to_string('store/email/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = "html" # Cho phep doc the HTML
            email.send(fail_silently=False)
            
            return render(request, 'store/auth/activation_sent.html')
    else:
        form = CustomRegisterForm()
        
    return render(request, 'store/auth/register.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Đã xác thực xong -> Lập tức tự Login cho họ luôn để tạo cảm xúc mượt mà
        login(request, user)
        sync_session_cart_to_db(request, user)
        return render(request, 'store/auth/activation_success.html')
    else:
        return render(request, 'store/auth/activation_invalid.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            sync_session_cart_to_db(request, user)
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
