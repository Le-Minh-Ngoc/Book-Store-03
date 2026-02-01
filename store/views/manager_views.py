from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from store.models import Book, Category, DamagedBook
from store.controllers.BookDAO.book_dao import BookDAO
from store.controllers.BookDAO.category_dao import CategoryDAO
from store.controllers.BookDAO.damaged_book_dao import DamagedBookDAO


@login_required
def manager_dashboard(request):
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    try:
        manager = request.user.staff_profile.manager_profile
    except:
        return redirect('book_list')
    
    books = BookDAO.get_all_books()
    total_books = books.count()
    low_stock_count = books.filter(quantity__lt=10, quantity__gt=0).count()
    out_of_stock_count = BookDAO.get_out_of_stock_books().count()
    damaged_count = DamagedBookDAO.get_all_damaged_books().count()
    
    low_stock_books = books.filter(quantity__lt=10, quantity__gt=0).order_by('quantity')[:10]
    
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
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    books = BookDAO.get_all_books()
    categories = CategoryDAO.get_all_categories()
    
    search = request.GET.get('search')
    if search:
        books = BookDAO.search_books(search)
    
    category = request.GET.get('category')
    if category:
        books = BookDAO.filter_by_category(category)
    
    stock_status = request.GET.get('stock_status')
    if stock_status == 'in_stock':
        books = BookDAO.get_books_in_stock()
    elif stock_status == 'low_stock':
        books = books.filter(quantity__lt=10, quantity__gt=0)
    elif stock_status == 'out_of_stock':
        books = BookDAO.get_out_of_stock_books()
    
    context = {
        'books': books,
        'categories': categories,
    }
    
    return render(request, 'manager/books.html', context)


@login_required
def manager_inventory_view(request):
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    books = BookDAO.get_all_books().order_by('quantity')
    
    context = {'books': books}
    return render(request, 'manager/inventory.html', context)


@login_required
def manager_damaged_books_view(request):
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    damaged_books = DamagedBookDAO.get_all_damaged_books()
    
    context = {'damaged_books': damaged_books}
    return render(request, 'manager/damaged_books.html', context)


@login_required
def manager_add_book_view(request):
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    return render(request, 'manager/add_book.html')


@login_required
def manager_edit_book_view(request, book_id):
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    book = BookDAO.get_book_by_id(book_id)
    if not book:
        return redirect('manager_books')
    
    context = {'book': book}
    return render(request, 'manager/edit_book.html', context)


@login_required
def manager_delete_book_view(request, book_id):
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    BookDAO.delete_book(book_id)
    
    return redirect('manager_books')
