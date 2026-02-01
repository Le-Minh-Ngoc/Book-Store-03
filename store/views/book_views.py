from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from store.models import Book, Category, Author, Publisher, Comment
from store.controllers.BookDAO.book_dao import BookDAO
from store.controllers.BookDAO.category_dao import CategoryDAO
from store.controllers.BookDAO.author_dao import AuthorDAO
from store.controllers.BookDAO.publisher_dao import PublisherDAO
from store.controllers.BookDAO.review_dao import ReviewDAO
from store.controllers.BookDAO.comment_dao import CommentDAO
from store.controllers.BookDAO.wishlist_dao import WishlistDAO
from store.controllers.UserDAO.history_dao import SearchHistoryDAO


def get_or_create_customer(user):
    if not hasattr(user, 'customer_profile'):
        from store.models import Customer
        customer = Customer.objects.create(
            user=user,
            tel=user.tel or ''
        )
        return customer
    return user.customer_profile


def book_list_view(request):
    books = BookDAO.get_all_books()
    
    category = request.GET.get('category')
    if category:
        books = BookDAO.filter_by_category(category)
    
    author = request.GET.get('author')
    if author:
        books = BookDAO.filter_by_author(author)
    
    search = request.GET.get('search')
    if search:
        if request.user.is_authenticated:
            SearchHistoryDAO.create_search_history(
                user=request.user,
                query=search
            )
        
        books = BookDAO.search_books(search)
    
    sort = request.GET.get('sort', 'title')
    if sort == 'price_asc':
        books = books.order_by('price')
    elif sort == 'price_desc':
        books = books.order_by('-price')
    elif sort == 'newest':
        books = books.order_by('-published_year')
    elif sort == 'popular':
        books = books.order_by('-sold_quantity')
    
    base_template = 'base/base.html'
    if request.user.is_authenticated and hasattr(request.user, 'staff_profile'):
        base_template = 'base/manager_base.html'

    context = {
        'books': books,
        'categories': CategoryDAO.get_all_categories(),
        'base_template': base_template
    }
    
    return render(request, 'books/book_list.html', context)


def book_detail_view(request, book_id):
    book = BookDAO.get_book_by_id(book_id)
    if not book:
        return JsonResponse({'error': 'Book not found'}, status=404)
    
    reviews = ReviewDAO.get_book_reviews(book)
    comments = CommentDAO.get_book_comments(book)
    
    avg_rating = ReviewDAO.get_average_rating(book)
    
    is_in_wishlist = False
    if request.user.is_authenticated and hasattr(request.user, 'customer_profile'):
        customer = request.user.customer_profile
        is_in_wishlist = WishlistDAO.is_in_wishlist(customer, book)
    
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
        book = BookDAO.get_book_by_id(book_id)
        if not book:
            return JsonResponse({'error': 'Book not found'}, status=404)
        
        customer = get_or_create_customer(request.user)
        
        rating = int(request.POST.get('rating'))
        comment_text = request.POST.get('comment', '')
        
        ReviewDAO.create_review(
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
        book = BookDAO.get_book_by_id(book_id)
        if not book:
            return JsonResponse({'error': 'Book not found'}, status=404)
        
        customer = get_or_create_customer(request.user)
        
        content = request.POST.get('content')
        
        CommentDAO.create_comment(
            customer=customer,
            book=book,
            content=content
        )
        
        return redirect('book_detail', book_id=book_id)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def toggle_wishlist(request, book_id):
    book = BookDAO.get_book_by_id(book_id)
    if not book:
        return JsonResponse({'error': 'Book not found'}, status=404)
    
    customer = get_or_create_customer(request.user)
    
    if WishlistDAO.is_in_wishlist(customer, book):
        WishlistDAO.remove_from_wishlist(customer, book)
        return JsonResponse({'status': 'removed'})
    else:
        WishlistDAO.add_to_wishlist(customer, book)
        return JsonResponse({'status': 'added'})


@login_required
def wishlist_view(request):
    customer = get_or_create_customer(request.user)
    wishlist_items = WishlistDAO.get_customer_wishlist(customer)
    
    return render(request, 'books/wishlist.html', {'wishlist_items': wishlist_items})


def category_list_view(request):
    categories = CategoryDAO.get_all_categories()
    return render(request, 'books/categories.html', {'categories': categories})


def author_list_view(request):
    authors = AuthorDAO.get_all_authors()
    return render(request, 'books/authors.html', {'authors': authors})


def author_detail_view(request, author_id):
    author = AuthorDAO.get_author_by_id(author_id)
    if not author:
        return JsonResponse({'error': 'Author not found'}, status=404)
    
    books = AuthorDAO.get_author_books(author)
    
    context = {
        'author': author,
        'books': books
    }
    
    return render(request, 'books/author_detail.html', context)


def publisher_list_view(request):
    publishers = PublisherDAO.get_all_publishers()
    return render(request, 'books/publishers.html', {'publishers': publishers})


def publisher_detail_view(request, publisher_id):
    publisher = PublisherDAO.get_publisher_by_id(publisher_id)
    if not publisher:
        return JsonResponse({'error': 'Publisher not found'}, status=404)
    
    books = PublisherDAO.get_publisher_books(publisher)
    
    context = {
        'publisher': publisher,
        'books': books
    }
    
    return render(request, 'books/publisher_detail.html', context)
