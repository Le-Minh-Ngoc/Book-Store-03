from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count, Sum
from store.models import User, Customer, Staff, Order, Payment, Shipping
from store.controllers.UserDAO.userdao import UserDAO
from store.controllers.UserDAO.customerdao import CustomerDAO
from store.controllers.UserDAO.staff_dao import StaffDAO
from store.controllers.OrderDAO.order_dao import OrderDAO
from store.controllers.OrderDAO.payment_dao import PaymentDAO
from store.controllers.OrderDAO.shipping_dao import ShippingDAO


def check_admin_permission(user):
    if user.is_superuser:
        return True
    if hasattr(user, 'staff_profile'):
        if hasattr(user.staff_profile, 'admin_profile') or hasattr(user.staff_profile, 'manager_profile'):
            return True
    return False


@login_required
def admin_dashboard(request):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    # Thống kê nhanh
    total_users = UserDAO.get_all_users().count()
    total_orders = OrderDAO.get_all_orders().count()
    pending_orders = OrderDAO.get_orders_by_status('pending').count()
    completed_orders = OrderDAO.get_orders_by_status('completed').count()
    total_revenue = OrderDAO.get_all_orders().filter(status='completed').aggregate(Sum('total'))['total__sum'] or 0
    
    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def admin_users_list_view(request):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    users = UserDAO.get_all_users()
    
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(fullname__icontains=search)
        )
    
    role_filter = request.GET.get('role')
    if role_filter == 'customer':
        users = users.filter(customer_profile__isnull=False)
    elif role_filter == 'staff':
        users = users.filter(staff_profile__isnull=False)
    elif role_filter == 'admin':
        users = users.filter(is_superuser=True)
    
    context = {
        'users': users
    }
    
    return render(request, 'admin/users_list.html', context)


@login_required
def admin_user_detail_view(request, user_id):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    user = UserDAO.get_user_by_id(user_id)
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    context = {
        'user': user,
        'is_customer': hasattr(user, 'customer_profile'),
        'is_staff': hasattr(user, 'staff_profile'),
    }
    
    if hasattr(user, 'customer_profile'):
        context['customer'] = user.customer_profile
        context['orders'] = user.customer_profile.orders.all()[:10]
    
    return render(request, 'admin/user_detail.html', context)


@login_required
def admin_toggle_user_status(request, user_id):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    user = UserDAO.get_user_by_id(user_id)
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    if user.id == request.user.id:
        return JsonResponse({'error': 'Cannot deactivate yourself'}, status=400)
    
    user.is_active = not user.is_active
    user.save()
    
    return JsonResponse({
        'status': 'success',
        'is_active': user.is_active
    })


@login_required
def admin_create_staff_view(request):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        fullname = request.POST.get('fullname', '')
        
        if UserDAO.user_exists(username=username):
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = UserDAO.create_user(
            username=username,
            email=email,
            password=password,
            fullname=fullname,
            is_staff=True
        )
        
        StaffDAO.create_staff(user=user)
        
        return redirect('admin_users_list')
    
    return render(request, 'admin/create_staff.html')


@login_required
def admin_orders_list_view(request):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    orders = OrderDAO.get_all_orders()
    
    status_filter = request.GET.get('status')
    if status_filter:
        orders = OrderDAO.get_orders_by_status(status_filter)
    
    search = request.GET.get('search')
    if search:
        orders = orders.filter(
            Q(id__icontains=search) |
            Q(customer__user__username__icontains=search)
        )
    
    total_revenue = orders.filter(status='completed').aggregate(Sum('total'))['total__sum'] or 0
    
    context = {
        'orders': orders,
        'total_revenue': total_revenue,
        'status_choices': ['pending', 'processing', 'shipped', 'delivered', 'cancelled', 'completed']
    }
    
    return render(request, 'admin/orders_list.html', context)


@login_required
def admin_order_detail_view(request, order_id):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    order = OrderDAO.get_order_by_id(order_id)
    if not order:
        return JsonResponse({'error': 'Order not found'}, status=404)
    
    order_items = OrderDAO.get_order_items(order)
    status_history = OrderDAO.get_order_status_history(order)
    
    context = {
        'order': order,
        'order_items': order_items,
        'status_history': status_history,
    }
    
    if hasattr(order, 'payment'):
        context['payment'] = order.payment
    
    if hasattr(order, 'shipping'):
        context['shipping'] = order.shipping
        context['tracking_history'] = ShippingDAO.get_tracking_history(order.shipping)
    
    return render(request, 'admin/order_detail.html', context)


@login_required
def admin_update_order_status(request, order_id):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        order = OrderDAO.get_order_by_id(order_id)
        if not order:
            return JsonResponse({'error': 'Order not found'}, status=404)
        
        new_status = request.POST.get('status')
        note = request.POST.get('note', '')
        
        OrderDAO.update_order_status(order, new_status, note)
        
        return redirect('admin_order_detail', order_id=order_id)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def admin_payments_list_view(request):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    payments = PaymentDAO.get_all_payments()
    
    status_filter = request.GET.get('status')
    if status_filter:
        payments = PaymentDAO.get_payments_by_status(status_filter)
    
    method_filter = request.GET.get('method')
    if method_filter:
        payments = PaymentDAO.get_payments_by_method(method_filter)
    
    total_amount = payments.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'payments': payments,
        'total_amount': total_amount,
        'status_choices': ['pending', 'completed', 'failed', 'refunded'],
        'method_choices': ['cash', 'card', 'bank_transfer', 'e_wallet']
    }
    
    return render(request, 'admin/payments_list.html', context)


@login_required
def admin_update_payment_status(request, payment_id):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        payment = PaymentDAO.get_payment_by_id(payment_id)
        if not payment:
            return JsonResponse({'error': 'Payment not found'}, status=404)
        
        new_status = request.POST.get('status')
        PaymentDAO.update_payment_status(payment, new_status)
        
        if new_status == 'completed':
            OrderDAO.update_order_status(payment.order, 'processing', 'Payment confirmed')
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def admin_shippings_list_view(request):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    shippings = ShippingDAO.get_all_shippings()
    
    status_filter = request.GET.get('status')
    if status_filter:
        shippings = ShippingDAO.get_shippings_by_status(status_filter)
    
    context = {
        'shippings': shippings,
        'status_choices': ['pending', 'assigned', 'picked_up', 'in_transit', 'shipped', 'delivered', 'failed'],
        'shippers': StaffDAO.get_all_shippers()
    }
    
    return render(request, 'admin/shippings_list.html', context)


@login_required
def admin_shipping_detail_view(request, shipping_id):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    shipping = ShippingDAO.get_shipping_by_id(shipping_id)
    if not shipping:
        return JsonResponse({'error': 'Shipping not found'}, status=404)
    
    tracking_history = ShippingDAO.get_tracking_history(shipping)
    
    context = {
        'shipping': shipping,
        'tracking_history': tracking_history,
        'order': shipping.order,
        'shippers': StaffDAO.get_all_shippers()
    }
    
    return render(request, 'admin/shipping_detail.html', context)


@login_required
def admin_update_shipping_status(request, shipping_id):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        shipping = ShippingDAO.get_shipping_by_id(shipping_id)
        if not shipping:
            return JsonResponse({'error': 'Shipping not found'}, status=404)
        
        new_status = request.POST.get('status')
        location = request.POST.get('location', 'In transit')
        note = request.POST.get('note', '')
        
        ShippingDAO.update_shipping_status(shipping, new_status)
        ShippingDAO.add_tracking(shipping, location, new_status, note)
        
        if new_status == 'delivered':
            OrderDAO.update_order_status(shipping.order, 'completed', 'Order delivered')
        
        return redirect('admin_shipping_detail', shipping_id=shipping_id)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def admin_assign_shipper(request, shipping_id):
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        shipping = ShippingDAO.get_shipping_by_id(shipping_id)
        if not shipping:
            return JsonResponse({'error': 'Shipping not found'}, status=404)
        
        shipper_id = request.POST.get('shipper_id')
        from store.models import Shipper
        shipper = get_object_or_404(Shipper, id=shipper_id)
        
        ShippingDAO.assign_shipper(shipping, shipper)
        ShippingDAO.update_shipping_status(shipping, 'assigned')
        
        return redirect('admin_shipping_detail', shipping_id=shipping_id)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
