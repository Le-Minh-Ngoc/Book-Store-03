from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Avg, Sum, F
from django.views.decorators.http import require_http_methods
from decimal import Decimal
from store.models import (
    User, Customer, Staff, MemberShip, Address, LoginHistory, Notification, SearchHistory,
    Book, Category, Author, Publisher, Review, Comment, Wishlist, DamagedBook,
    Cart, CartItem, Order, OrderItem, OrderStatus, Payment, Voucher, Invoice, InvoiceItem,
    Shipping, ShippingAddress, Warehouse, ImportSlip, ImportSlipDetail, Supplier
)
from store.services.recommendation_service import BookRecommendationService


def get_or_create_customer(user):
    """Helper function để tạo customer profile nếu chưa có"""
    if not hasattr(user, 'customer_profile'):
        customer = Customer.objects.create(
            user=user,
            tel=user.tel or ''
        )
        return customer
    return user.customer_profile


def home_view(request):
    return redirect('book_list')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        fullname = request.POST.get('fullname', '')
        tel = request.POST.get('tel', '')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            fullname=fullname,
            tel=tel
        )
        
        Customer.objects.create(user=user, tel=tel)
        
        return redirect('login')
    
    return render(request, 'users/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
            device = request.META.get('HTTP_USER_AGENT', 'Unknown')
            LoginHistory.objects.create(user=user, ip_address=ip, device=device)
            
            # Redirect dựa trên role
            if user.is_superuser:
                return redirect('/admin/')
            elif hasattr(user, 'staff_profile'):
                # Kiểm tra nếu là manager
                try:
                    manager = user.staff_profile.manager_profile
                    return redirect('manager_dashboard')
                except:
                    # Staff khác
                    return redirect('book_list')
            else:
                # Customer thường
                return redirect('book_list')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'users/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user
    }
    
    if hasattr(user, 'customer_profile'):
        context['customer'] = user.customer_profile
        context['addresses'] = user.customer_profile.addresses.all()
        context['memberships'] = user.customer_profile.memberships.all()
    
    return render(request, 'users/profile.html', context)


@login_required
def update_profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.fullname = request.POST.get('fullname', user.fullname)
        user.tel = request.POST.get('tel', user.tel)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        return redirect('profile')
    
    return render(request, 'users/update_profile.html')


@login_required
def add_address_view(request):
    # Kiểm tra xem user có customer profile chưa
    if not hasattr(request.user, 'customer_profile'):
        from django.contrib import messages
        messages.error(request, 'Bạn cần phải là khách hàng để thêm địa chỉ.')
        return redirect('profile')
    
    if request.method == 'POST':
        from django.contrib import messages
        
        try:
            customer = request.user.customer_profile
            
            Address.objects.create(
                customer=customer,
                num=request.POST.get('num'),
                street=request.POST.get('street'),
                city=request.POST.get('city'),
                country=request.POST.get('country', 'Việt Nam')
            )
            
            messages.success(request, 'Đã thêm địa chỉ thành công!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')
    
    return render(request, 'users/add_address.html')


@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()
    return render(request, 'users/notifications.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})


@login_required
def login_history_view(request):
    history = request.user.login_histories.all()[:20]
    return render(request, 'users/login_history.html', {'history': history})


@login_required
def search_history_view(request):
    history = request.user.search_histories.all()[:50]
    return render(request, 'users/search_history.html', {'history': history})


def book_list_view(request):
    books = Book.objects.all()
    
    category = request.GET.get('category')
    if category:
        books = books.filter(categories__type=category)
    
    author = request.GET.get('author')
    if author:
        books = books.filter(authors__name__icontains=author)
    
    search = request.GET.get('search')
    if search:
        # Lưu lịch sử tìm kiếm cho user đã đăng nhập
        if request.user.is_authenticated:
            SearchHistory.objects.create(
                user=request.user,
                query=search
            )
        
        # Tìm kiếm theo: tên sách, mô tả, ISBN, tác giả, nhà xuất bản
        books = books.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(ISBN__icontains=search) |
            Q(authors__name__icontains=search) |
            Q(publisher__name__icontains=search)
        ).distinct()
    
    sort = request.GET.get('sort', 'title')
    if sort == 'price_asc':
        books = books.order_by('price')
    elif sort == 'price_desc':
        books = books.order_by('-price')
    elif sort == 'newest':
        books = books.order_by('-published_year')
    elif sort == 'popular':
        books = books.order_by('-sold_quantity')
    
    context = {
        'books': books,
        'categories': Category.objects.all()
    }
    
    return render(request, 'books/book_list.html', context)


def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()
    comments = book.comments.all()
    
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    is_in_wishlist = False
    if request.user.is_authenticated and hasattr(request.user, 'customer_profile'):
        is_in_wishlist = Wishlist.objects.filter(
            customer=request.user.customer_profile,
            book=book
        ).exists()
    
    context = {
        'book': book,
        'reviews': reviews,
        'comments': comments,
        'avg_rating': avg_rating,
        'is_in_wishlist': is_in_wishlist
    }
    
    return render(request, 'books/book_detail.html', context)


@login_required
def add_review(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        customer = get_or_create_customer(request.user)
        
        rating = int(request.POST.get('rating'))
        comment_text = request.POST.get('comment', '')
        
        Review.objects.create(
            customer=customer,
            book=book,
            rating=rating,
            comment=comment_text
        )
        
        return redirect('book_detail', book_id=book_id)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def add_comment(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        customer = get_or_create_customer(request.user)
        
        content = request.POST.get('content')
        
        Comment.objects.create(
            customer=customer,
            book=book,
            content=content
        )
        
        return redirect('book_detail', book_id=book_id)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def toggle_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    customer = get_or_create_customer(request.user)
    
    wishlist_item = Wishlist.objects.filter(customer=customer, book=book)
    
    if wishlist_item.exists():
        wishlist_item.delete()
        return JsonResponse({'status': 'removed'})
    else:
        Wishlist.objects.create(customer=customer, book=book)
        return JsonResponse({'status': 'added'})


@login_required
def wishlist_view(request):
    customer = get_or_create_customer(request.user)
    wishlist_items = customer.wishlists.all()
    
    return render(request, 'books/wishlist.html', {'wishlist_items': wishlist_items})


def category_list_view(request):
    categories = Category.objects.all()
    return render(request, 'books/categories.html', {'categories': categories})


def author_list_view(request):
    authors = Author.objects.all()
    return render(request, 'books/authors.html', {'authors': authors})


def author_detail_view(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all()
    
    context = {
        'author': author,
        'books': books
    }
    
    return render(request, 'books/author_detail.html', context)


def publisher_list_view(request):
    publishers = Publisher.objects.all()
    return render(request, 'books/publishers.html', {'publishers': publishers})


def publisher_detail_view(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    books = publisher.books.all()
    
    context = {
        'publisher': publisher,
        'books': books
    }
    
    return render(request, 'books/publisher_detail.html', context)


@login_required
def cart_view(request):
    customer = get_or_create_customer(request.user)
    
    cart, created = Cart.objects.get_or_create(
        customer=customer,
        defaults={'id': f'CART-{customer.id}'}
    )
    
    cart_items = cart.items.all()
    
    total = sum(item.book.price * item.quantity for item in cart_items)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total
    }
    
    return render(request, 'orders/cart.html', context)


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    customer = get_or_create_customer(request.user)
    
    cart, created = Cart.objects.get_or_create(
        customer=customer,
        defaults={'id': f'CART-{customer.id}'}
    )
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    cart_total = sum(item.book.price * item.quantity for item in cart.items.all())
    cart.total_price = cart_total
    cart.save()
    
    return redirect('cart')


@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        cart = cart_item.cart
        cart_total = sum(item.book.price * item.quantity for item in cart.items.all())
        cart.total_price = cart_total
        cart.save()
        
        return redirect('cart')
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart
    cart_item.delete()
    
    cart_total = sum(item.book.price * item.quantity for item in cart.items.all())
    cart.total_price = cart_total
    cart.save()
    
    return redirect('cart')


@login_required
def checkout_view(request):
    customer = get_or_create_customer(request.user)
    cart = get_object_or_404(Cart, customer=customer)
    cart_items = cart.items.all()
    
    if not cart_items:
        return redirect('cart')
    
    total = sum(item.book.price * item.quantity for item in cart_items)
    
    addresses = customer.addresses.all()
    
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
        cart = get_object_or_404(Cart, customer=customer)
        cart_items = cart.items.all()
        
        if not cart_items:
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        total = sum(item.book.price * item.quantity for item in cart_items)
        
        import uuid
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        order = Order.objects.create(
            id=order_id,
            customer=customer,
            total=total,
            status='pending'
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            
            item.book.quantity -= item.quantity
            item.book.sold_quantity += item.quantity
            item.book.save()
        
        OrderStatus.objects.create(
            order=order,
            status='pending',
            note='Order placed'
        )
        
        cart_items.delete()
        cart.total_price = 0
        cart.save()
        
        payment_method = request.POST.get('payment_method', 'cash')
        payment_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"
        
        Payment.objects.create(
            id=payment_id,
            order=order,
            amount=total,
            method=payment_method,
            status='pending'
        )
        
        return redirect('order_detail', order_id=order_id)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def order_list_view(request):
    customer = get_or_create_customer(request.user)
    orders = customer.orders.all()
    
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if order.customer != get_or_create_customer(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    order_items = order.items.all()
    
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
        
        try:
            voucher = Voucher.objects.get(code=code)
            
            from django.utils import timezone
            today = timezone.now().date()
            
            if voucher.start_date <= today <= voucher.end_date:
                return JsonResponse({
                    'status': 'success',
                    'discount_percent': str(voucher.discount_percent),
                    'min_order_value': str(voucher.min_order_value)
                })
            else:
                return JsonResponse({'error': 'Voucher expired'}, status=400)
        except Voucher.DoesNotExist:
            return JsonResponse({'error': 'Invalid voucher code'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if order.customer != get_or_create_customer(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if order.status in ['pending', 'processing']:
        order.status = 'cancelled'
        order.save()
        
        OrderStatus.objects.create(
            order=order,
            status='cancelled',
            note='Cancelled by customer'
        )
        
        for item in order.items.all():
            item.book.quantity += item.quantity
            item.book.sold_quantity -= item.quantity
            item.book.save()
        
        return redirect('order_list')
    
    return JsonResponse({'error': 'Cannot cancel order'}, status=400)


@login_required
def warehouse_list_view(request):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    warehouses = Warehouse.objects.all()
    return render(request, 'warehouse/warehouse_list.html', {'warehouses': warehouses})


@login_required
def warehouse_detail_view(request, warehouse_id):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    import_slips = warehouse.import_slips.all()
    
    context = {
        'warehouse': warehouse,
        'import_slips': import_slips
    }
    
    return render(request, 'warehouse/warehouse_detail.html', context)


@login_required
def import_slip_list_view(request):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    import_slips = ImportSlip.objects.all()
    return render(request, 'warehouse/import_slip_list.html', {'import_slips': import_slips})


@login_required
def import_slip_detail_view(request, slip_id):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    import_slip = get_object_or_404(ImportSlip, id=slip_id)
    details = import_slip.details.all()
    
    context = {
        'import_slip': import_slip,
        'details': details
    }
    
    return render(request, 'warehouse/import_slip_detail.html', context)


@login_required
def create_import_slip_view(request):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        import uuid
        slip_id = f"IMP-{uuid.uuid4().hex[:8].upper()}"
        
        supplier_id = request.POST.get('supplier_id')
        warehouse_id = request.POST.get('warehouse_id')
        
        supplier = get_object_or_404(Supplier, id=supplier_id)
        warehouse = get_object_or_404(Warehouse, id=warehouse_id)
        
        manager = None
        if hasattr(request.user.staff_profile, 'manager_profile'):
            manager = request.user.staff_profile.manager_profile
        
        import_slip = ImportSlip.objects.create(
            id=slip_id,
            supplier=supplier,
            warehouse=warehouse,
            manager=manager,
            total=0
        )
        
        return redirect('import_slip_detail', slip_id=slip_id)
    
    suppliers = Supplier.objects.all()
    warehouses = Warehouse.objects.all()
    
    context = {
        'suppliers': suppliers,
        'warehouses': warehouses
    }
    
    return render(request, 'warehouse/create_import_slip.html', context)


@login_required
def add_import_detail(request, slip_id):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        import_slip = get_object_or_404(ImportSlip, id=slip_id)
        
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        
        book = get_object_or_404(Book, id=book_id)
        
        total = quantity * price
        
        ImportSlipDetail.objects.create(
            import_slip=import_slip,
            book=book,
            quantity=quantity,
            price=price,
            total=total
        )
        
        book.quantity += quantity
        book.save()
        
        import_slip.total = sum(detail.total for detail in import_slip.details.all())
        import_slip.save()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def inventory_view(request):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    books = Book.objects.all().order_by('title')
    
    search = request.GET.get('search')
    if search:
        books = books.filter(title__icontains=search)
    
    low_stock = request.GET.get('low_stock')
    if low_stock:
        books = books.filter(quantity__lt=10)
    
    context = {
        'books': books
    }
    
    return render(request, 'warehouse/inventory.html', context)


# Recommendation views
def recommendations_view(request):
    """Trang hiển thị sách được gợi ý cho user"""
    recommendation_service = BookRecommendationService(request.user)
    
    recommended_books = recommendation_service.get_recommended_books(limit=12)
    trending_books = recommendation_service.get_trending_books(limit=10)
    new_arrivals = recommendation_service.get_new_arrivals(limit=10)
    
    context = {
        'recommended_books': recommended_books,
        'trending_books': trending_books,
        'new_arrivals': new_arrivals,
    }
    
    return render(request, 'books/recommendations.html', context)


@require_http_methods(["GET"])
def get_similar_books_api(request, book_id):
    """API để lấy sách tương tự"""
    book = get_object_or_404(Book, id=book_id)
    recommendation_service = BookRecommendationService(request.user)
    
    similar_books = recommendation_service.get_similar_books(book, limit=6)
    
    books_data = [{
        'id': book.id,
        'title': book.title,
        'price': float(book.price),
        'image_url': book.image_url,
        'authors': ', '.join([author.name for author in book.authors.all()])
    } for book in similar_books]
    
    return JsonResponse({'similar_books': books_data})


# Manager views
@login_required
def manager_dashboard(request):
    """Dashboard cho Manager"""
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    try:
        manager = request.user.staff_profile.manager_profile
    except:
        return redirect('book_list')
    
    # Thống kê
    total_books = Book.objects.count()
    low_stock_count = Book.objects.filter(quantity__lt=10, quantity__gt=0).count()
    out_of_stock_count = Book.objects.filter(quantity=0).count()
    damaged_count = DamagedBook.objects.count()
    
    # Sách sắp hết hàng
    low_stock_books = Book.objects.filter(quantity__lt=10, quantity__gt=0).order_by('quantity')[:10]
    
    context = {
        'total_books': total_books,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'damaged_count': damaged_count,
        'low_stock_books': low_stock_books,
    }
    
    return render(request, 'manager/dashboard.html', context)


@login_required
def manager_books_view(request):
    """Quản lý sách"""
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    books = Book.objects.all()
    categories = Category.objects.all()
    
    # Filter
    search = request.GET.get('search')
    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(authors__name__icontains=search)
        ).distinct()
    
    category = request.GET.get('category')
    if category:
        books = books.filter(categories__type=category)
    
    stock_status = request.GET.get('stock_status')
    if stock_status == 'in_stock':
        books = books.filter(quantity__gt=0)
    elif stock_status == 'low_stock':
        books = books.filter(quantity__lt=10, quantity__gt=0)
    elif stock_status == 'out_of_stock':
        books = books.filter(quantity=0)
    
    context = {
        'books': books,
        'categories': categories,
    }
    
    return render(request, 'manager/books.html', context)


@login_required
def manager_inventory_view(request):
    """Kiểm tra tồn kho"""
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    books = Book.objects.all().order_by('quantity')
    
    context = {'books': books}
    return render(request, 'manager/inventory.html', context)


@login_required
def manager_damaged_books_view(request):
    """Quản lý sách lỗi"""
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    damaged_books = DamagedBook.objects.all()
    
    context = {'damaged_books': damaged_books}
    return render(request, 'manager/damaged_books.html', context)


@login_required
def manager_add_book_view(request):
    """Thêm sách mới"""
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    # TODO: Implement form
    return render(request, 'manager/add_book.html')


@login_required
def manager_edit_book_view(request, book_id):
    """Sửa thông tin sách"""
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    book = get_object_or_404(Book, id=book_id)
    # TODO: Implement form
    
    context = {'book': book}
    return render(request, 'manager/edit_book.html', context)


@login_required
def manager_delete_book_view(request, book_id):
    """Xóa sách"""
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    
    return redirect('manager_books')
