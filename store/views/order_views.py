from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models.order import Order

@login_required(login_url='/admin/login/')
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders/order_list.html', {'orders': orders})

@login_required(login_url='/admin/login/')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/orders/order_detail.html', {'order': order})
