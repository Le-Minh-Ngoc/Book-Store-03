from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models import User, Customer, Address
from store.controllers.UserDAO.userdao import UserDAO
from store.controllers.UserDAO.customerdao import CustomerDAO
from store.controllers.UserDAO.history_dao import LoginHistoryDAO, SearchHistoryDAO
from store.controllers.UserDAO.notification_dao import NotificationDAO


def get_or_create_customer(user):
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
        
        if UserDAO.user_exists(username=username):
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        if UserDAO.user_exists(email=email):
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        user = UserDAO.create_user(
            username=username,
            email=email,
            password=password,
            fullname=fullname,
            tel=tel
        )
        
        CustomerDAO.create_customer(user=user, tel=tel)
        
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
            LoginHistoryDAO.create_login_history(user=user, ip_address=ip, device=device)
            
            if user.is_superuser:
                return redirect('/admin/')
            elif hasattr(user, 'staff_profile'):
                try:
                    manager = user.staff_profile.manager_profile
                    return redirect('manager_dashboard')
                except:
                    return redirect('book_list')
            else:
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
        customer = user.customer_profile
        context['customer'] = customer
        context['addresses'] = CustomerDAO.get_customer_addresses(customer)
        context['memberships'] = CustomerDAO.get_customer_memberships(customer)
    
    return render(request, 'users/profile.html', context)


@login_required
def update_profile_view(request):
    if request.method == 'POST':
        user = request.user
        UserDAO.update_user(
            user.id,
            fullname=request.POST.get('fullname', user.fullname),
            tel=request.POST.get('tel', user.tel),
            email=request.POST.get('email', user.email)
        )
        
        return redirect('profile')
    
    return render(request, 'users/update_profile.html')


@login_required
def add_address_view(request):
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
    notifications = NotificationDAO.get_user_notifications(request.user)
    return render(request, 'users/notifications.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, notification_id):
    NotificationDAO.mark_as_read(notification_id)
    return JsonResponse({'status': 'success'})


@login_required
def login_history_view(request):
    history = LoginHistoryDAO.get_user_login_history(request.user, limit=20)
    return render(request, 'users/login_history.html', {'history': history})


@login_required
def search_history_view(request):
    history = SearchHistoryDAO.get_user_search_history(request.user, limit=50)
    return render(request, 'users/search_history.html', {'history': history})
