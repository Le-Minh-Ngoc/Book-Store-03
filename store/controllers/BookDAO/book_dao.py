from store.models import Book
from django.db.models import Q
from django.db import transaction


class BookDAO:
    
    @staticmethod
    def create_book(book_data):
        with transaction.atomic():
            authors = book_data.pop('authors', [])
            categories = book_data.pop('categories', [])
            
            book = Book.objects.create(**book_data)
            
            if authors:
                book.authors.set(authors)
            
            if categories:
                book.categories.set(categories)
            
            return book
    
    @staticmethod
    def get_book_by_id(book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_books():
        return Book.objects.all()
    
    @staticmethod
    def search_books(query):
        return Book.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ISBN__icontains=query)
        )
    
    @staticmethod
    def filter_by_category(category_type):
        return Book.objects.filter(categories__type=category_type)
    
    @staticmethod
    def filter_by_author(author_name):
        return Book.objects.filter(authors__name__icontains=author_name)
    
    @staticmethod
    def filter_by_publisher(publisher_id):
        return Book.objects.filter(publisher_id=publisher_id)
    
    @staticmethod
    def filter_by_price_range(min_price, max_price):
        return Book.objects.filter(price__gte=min_price, price__lte=max_price)
    
    @staticmethod
    def get_popular_books(limit=10):
        return Book.objects.order_by('-sold_quantity')[:limit]
    
    @staticmethod
    def get_new_books(limit=10):
        return Book.objects.order_by('-published_year')[:limit]
    
    @staticmethod
    def get_books_in_stock():
        return Book.objects.filter(quantity__gt=0)
    
    @staticmethod
    def get_out_of_stock_books():
        return Book.objects.filter(quantity=0)
    
    @staticmethod
    def update_book(book_id, **kwargs):
        book = Book.objects.get(id=book_id)
        
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        
        book.save()
        return book
    
    @staticmethod
    def delete_book(book_id):
        book = Book.objects.get(id=book_id)
        book.delete()
    
    @staticmethod
    def update_quantity(book_id, quantity_change):
        book = Book.objects.get(id=book_id)
        book.quantity += quantity_change
        book.save()
        return book
    
    @staticmethod
    def update_sold_quantity(book_id, quantity_sold):
        book = Book.objects.get(id=book_id)
        book.sold_quantity += quantity_sold
        book.quantity -= quantity_sold
        book.save()
        return book
    
    @staticmethod
    def get_stock_status(book):
        if book.quantity == 0:
            return 'out_of_stock'
        elif book.quantity < 10:
            return 'low_stock'
        else:
            return 'in_stock'
