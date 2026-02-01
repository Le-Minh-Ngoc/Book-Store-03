from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from store.models import Book, Category, DamagedBook
from store.controllers.BookDAO.book_dao import BookDAO
from store.controllers.BookDAO.category_dao import CategoryDAO
from store.controllers.BookDAO.damaged_book_dao import DamagedBookDAO
from store.controllers.BookDAO.author_dao import AuthorDAO
from store.controllers.BookDAO.publisher_dao import PublisherDAO
from django.contrib import messages


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
        
    if request.method == 'POST':
        try:
            # Handle new author creation if provided
            new_author_id = request.POST.get('new_author_id')
            if new_author_id:
                new_author_data = {
                    'id': new_author_id,
                    'name': request.POST.get('new_author_name'),
                    'birthdate': request.POST.get('new_author_birthdate'),
                    'country': request.POST.get('new_author_country'),
                    'address': request.POST.get('new_author_address'),
                    'biography': ''
                }
                AuthorDAO.create_author(new_author_data)
            
            # Get selected authors
            selected_authors = request.POST.getlist('authors')
            if new_author_id:
                selected_authors.append(new_author_id)

            book_data = {
                'id': request.POST.get('id'),
                'title': request.POST.get('title'),
                'ISBN': request.POST.get('isbn'),
                'price': request.POST.get('price'),
                'quantity': request.POST.get('quantity'),
                'description': request.POST.get('description'),
                'publisher_id': request.POST.get('publisher'),
                'published_year': request.POST.get('published_year'),
                'page_count': request.POST.get('page_count'),
                'language': request.POST.get('language'),
                'image_url': request.POST.get('image_url') or None,
                'categories': request.POST.getlist('categories'),
                'authors': selected_authors,
            }
            
            # Check for duplicates before creating
            if Book.objects.filter(id=book_data['id']).exists():
                messages.error(request, f"Mã sách '{book_data['id']}' đã tồn tại.")
            elif Book.objects.filter(ISBN=book_data['ISBN']).exists():
                messages.error(request, f"ISBN '{book_data['ISBN']}' đã tồn tại.")
            else:
                BookDAO.create_book(book_data)
                messages.success(request, 'Thêm sách mới thành công!')
                return redirect('manager_books')
                
        except Exception as e:
            error_msg = str(e)
            if 'Duplicate entry' in error_msg:
                if 'book.ISBN' in error_msg:
                    messages.error(request, 'ISBN này đã được sử dụng cho sách khác.')
                elif 'book.id' in error_msg:
                    messages.error(request, 'Mã sách (ID) này đã tồn tại.')
                else:
                    messages.error(request, f'Dữ liệu bị trùng lặp: {error_msg}')
            else:
                messages.error(request, f'Lỗi khi thêm sách: {error_msg}')
    
    context = {
        'categories': CategoryDAO.get_all_categories(),
        'authors': AuthorDAO.get_all_authors(),
        'publishers': PublisherDAO.get_all_publishers(),
    }
    return render(request, 'manager/add_book.html', context)


@login_required
def manager_edit_book_view(request, book_id):
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    book = BookDAO.get_book_by_id(book_id)
    if not book:
        return redirect('manager_books')
        
    if request.method == 'POST':
        try:
            # Handle new author creation if provided
            new_author_id = request.POST.get('new_author_id')
            if new_author_id:
                new_author_data = {
                    'id': new_author_id,
                    'name': request.POST.get('new_author_name'),
                    'birthdate': request.POST.get('new_author_birthdate'),
                    'country': request.POST.get('new_author_country'),
                    'address': request.POST.get('new_author_address'),
                    'biography': ''
                }
                AuthorDAO.create_author(new_author_data)

            # Update basic fields
            book.title = request.POST.get('title')
            book.price = request.POST.get('price')
            book.quantity = request.POST.get('quantity')
            book.description = request.POST.get('description')
            book.publisher_id = request.POST.get('publisher')
            book.published_year = request.POST.get('published_year')
            book.page_count = request.POST.get('page_count')
            book.language = request.POST.get('language')
            
            image_url = request.POST.get('image_url')
            if image_url:
                book.image_url = image_url
            
            book.save()
            
            # Update M2M relationships
            categories = request.POST.getlist('categories')
            if categories:
                book.categories.set(categories)
                
            authors = request.POST.getlist('authors')
            if new_author_id:
                authors.append(new_author_id)
                
            if authors:
                book.authors.set(authors)
            
            messages.success(request, 'Cập nhật sách thành công')
            return redirect('manager_books')
        except Exception as e:
            messages.error(request, f'Lỗi khi cập nhật sách: {str(e)}')
    
    context = {
        'book': book,
        'categories': CategoryDAO.get_all_categories(),
        'authors': AuthorDAO.get_all_authors(),
        'publishers': PublisherDAO.get_all_publishers(),
    }
    return render(request, 'manager/edit_book.html', context)


@login_required
def manager_delete_book_view(request, book_id):
    if not hasattr(request.user, 'staff_profile'):
        return redirect('book_list')
    
    BookDAO.delete_book(book_id)
    
    return redirect('manager_books')
