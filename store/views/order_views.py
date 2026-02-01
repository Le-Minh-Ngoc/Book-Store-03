from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models import Customer
from store.controllers.CartDAO.cart_dao import CartDAO
from store.controllers.OrderDAO.order_dao import OrderDAO
from store.controllers.OrderDAO.payment_dao import PaymentDAO
from store.controllers.OrderDAO.voucher_dao import VoucherDAO
from store.controllers.BookDAO.book_dao import BookDAO
from store.controllers.UserDAO.customerdao import CustomerDAO
import uuid


def get_or_create_customer(user):
    if not hasattr(user, 'customer_profile'):
        customer = Customer.objects.create(
            user=user,
            tel=user.tel or ''
        )
        return customer
    return user.customer_profile


@login_required
def cart_view(request):
    customer = get_or_create_customer(request.user)
    cart = CartDAO.get_or_create_cart(customer)
    cart_items = CartDAO.get_cart_items(cart)
    total = CartDAO.get_cart_total(cart)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total
    }
    
    return render(request, 'orders/cart.html', context)


@login_required
def add_to_cart(request, book_id):
    book = BookDAO.get_book_by_id(book_id)
    if not book:
        return JsonResponse({'error': 'Book not found'}, status=404)
    
    customer = get_or_create_customer(request.user)
    cart = CartDAO.get_or_create_cart(customer)
    
    quantity = int(request.POST.get('quantity', 1))
    
    CartDAO.add_item(cart, book, quantity)
    
    return redirect('cart')


@login_required
def update_cart_item(request, item_id):
    from store.models import CartItem
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        CartDAO.update_item_quantity(cart_item, quantity)
        
        return redirect('cart')
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def remove_from_cart(request, item_id):
    from store.models import CartItem
    cart_item = get_object_or_404(CartItem, id=item_id)
    CartDAO.remove_item(cart_item)
    
    return redirect('cart')


@login_required
def checkout_view(request):
    customer = get_or_create_customer(request.user)
    cart = CartDAO.get_cart_by_customer(customer)
    
    if not cart:
        return redirect('cart')
    
    cart_items = CartDAO.get_cart_items(cart)
    
    if not cart_items:
        return redirect('cart')
    
    total = CartDAO.get_cart_total(cart)
    addresses = CustomerDAO.get_customer_addresses(customer)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'addresses': addresses
    }
    
    return render(request, 'orders/checkout.html', context)


@login_required
def place_order(request):
    if request.method == 'POST':
        customer = get_or_create_customer(request.user)
        cart = CartDAO.get_cart_by_customer(customer)
        
        if not cart:
            return JsonResponse({'error': 'Cart not found'}, status=400)
        
        cart_items = CartDAO.get_cart_items(cart)
        
        if not cart_items:
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        total = CartDAO.get_cart_total(cart)
        
        order = OrderDAO.create_order(customer, total, status='pending')
        
        for item in cart_items:
            OrderDAO.add_order_item(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            
            BookDAO.update_sold_quantity(item.book.id, item.quantity)
        
        OrderDAO.update_order_status(order, 'pending', 'Order placed')
        
        CartDAO.clear_cart(cart)
        
        payment_method = request.POST.get('payment_method', 'cash')
        payment_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"
        
        PaymentDAO.create_payment(
            payment_id=payment_id,
            order=order,
            amount=total,
            method=payment_method,
            status='pending'
        )
        
        return redirect('order_detail', order_id=order.id)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def order_list_view(request):
    customer = get_or_create_customer(request.user)
    orders = OrderDAO.get_customer_orders(customer)
    
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = OrderDAO.get_order_by_id(order_id)
    
    if not order:
        return JsonResponse({'error': 'Order not found'}, status=404)
    
    customer = get_or_create_customer(request.user)
    if order.customer != customer:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    order_items = OrderDAO.get_order_items(order)
    
    context = {
        'order': order,
        'order_items': order_items
    }
    
    if hasattr(order, 'payment'):
        context['payment'] = order.payment
    
    if hasattr(order, 'shipping'):
        context['shipping'] = order.shipping
    
    if hasattr(order, 'invoice'):
        context['invoice'] = order.invoice
    
    return render(request, 'orders/order_detail.html', context)


@login_required
def apply_voucher(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        
        voucher = VoucherDAO.get_voucher_by_code(code)
        
        if not voucher:
            return JsonResponse({'error': 'Invalid voucher code'}, status=400)
        
        if VoucherDAO.is_voucher_valid(voucher):
            return JsonResponse({
                'status': 'success',
                'discount_percent': str(voucher.discount_percent),
                'min_order_value': str(voucher.min_order_value)
            })
        else:
            return JsonResponse({'error': 'Voucher expired'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def cancel_order(request, order_id):
    order = OrderDAO.get_order_by_id(order_id)
    
    if not order:
        return JsonResponse({'error': 'Order not found'}, status=404)
    
    customer = get_or_create_customer(request.user)
    if order.customer != customer:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if OrderDAO.cancel_order(order):
        return redirect('order_list')
    
    return JsonResponse({'error': 'Cannot cancel order'}, status=400)


@login_required
def track_order_view(request, order_id):
    customer = get_or_create_customer(request.user)
    order = OrderDAO.get_order_by_id(order_id)
    
    if not order or order.customer != customer:
        return JsonResponse({'error': 'Order not found'}, status=404)
    
    context = {
        'order': order,
        'order_items': OrderDAO.get_order_items(order),
        'status_history': OrderDAO.get_order_status_history(order),
    }
    
    if hasattr(order, 'shipping'):
        from store.controllers.OrderDAO.shipping_dao import ShippingDAO
        context['shipping'] = order.shipping
        context['tracking_history'] = ShippingDAO.get_tracking_history(order.shipping)
        context['shipping_address'] = ShippingDAO.get_shipping_address(order.shipping)
    
    if hasattr(order, 'payment'):
        context['payment'] = order.payment
    
    return render(request, 'orders/track_order.html', context)


@login_required
def track_by_number_view(request):
    tracking_number = request.GET.get('tracking_number')
    
    if not tracking_number:
        return render(request, 'orders/track_by_number.html', {'error': 'Please enter tracking number'})
    
    from store.controllers.OrderDAO.shipping_dao import ShippingDAO
    shipping = ShippingDAO.get_shipping_by_tracking(tracking_number)
    
    if not shipping:
        return render(request, 'orders/track_by_number.html', {'error': 'Tracking number not found'})
    
    customer = get_or_create_customer(request.user)
    if shipping.order.customer != customer:
        return render(request, 'orders/track_by_number.html', {'error': 'Unauthorized'})
    
    context = {
        'shipping': shipping,
        'order': shipping.order,
        'tracking_history': ShippingDAO.get_tracking_history(shipping),
        'shipping_address': ShippingDAO.get_shipping_address(shipping),
    }
    
    return render(request, 'orders/track_by_number.html', context)
