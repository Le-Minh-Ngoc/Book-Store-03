from django.db.models import Q, Count
from store.models import Book, Wishlist, OrderItem, SearchHistory


class BookRecommendationService:
    """Service để gợi ý sách cho người dùng"""
    
    def __init__(self, user):
        self.user = user
    
    def get_recommended_books(self, limit=12):
        """Lấy danh sách sách được gợi ý"""
        if not self.user.is_authenticated:
            return list(self._get_popular_books(limit))
        
        # Lấy sách từ các nguồn khác nhau
        wishlist_books = self._get_books_from_wishlist()
        order_books = self._get_books_from_orders()
        search_books = self._get_books_from_search()
        
        # Lấy categories và authors từ sách user đã tương tác
        interested_categories = set()
        interested_authors = set()
        viewed_books = set()
        
        all_books = set(wishlist_books) | set(order_books) | set(search_books)
        
        for book in all_books:
            viewed_books.add(book.id)
            interested_categories.update(book.categories.all())
            interested_authors.update(book.authors.all())
        
        # Nếu không có sở thích, trả về sách phổ biến
        if not interested_categories and not interested_authors:
            return list(self._get_popular_books(limit))
        
        # Tìm sách tương tự - KHÔNG dùng slicing trực tiếp
        recommended_qs = Book.objects.filter(
            Q(categories__in=interested_categories) | 
            Q(authors__in=interested_authors)
        ).exclude(
            id__in=viewed_books
        ).distinct().order_by('-sold_quantity', '-quantity')
        
        # Convert sang list và slice
        recommended = list(recommended_qs)[:limit]
        
        # Nếu không đủ, lấy thêm sách phổ biến
        if len(recommended) < limit:
            popular_qs = self._get_popular_books(limit - len(recommended))
            popular_books = [b for b in popular_qs if b.id not in [r.id for r in recommended]]
            recommended = recommended + popular_books
        
        return recommended
    
    def _get_books_from_wishlist(self):
        """Lấy sách từ wishlist"""
        if not hasattr(self.user, 'customer_profile'):
            return []
        
        # Lấy book IDs từ wishlist
        wishlist_items = list(Wishlist.objects.filter(
            customer=self.user.customer_profile
        ).values_list('book_id', flat=True)[:10])
        
        return list(Book.objects.filter(id__in=wishlist_items))
    
    def _get_books_from_orders(self):
        """Lấy sách từ lịch sử đơn hàng"""
        if not hasattr(self.user, 'customer_profile'):
            return []
        
        # Lấy book IDs từ orders
        order_book_ids = list(OrderItem.objects.filter(
            order__customer=self.user.customer_profile
        ).values_list('book_id', flat=True)[:20])
        
        return list(Book.objects.filter(id__in=order_book_ids))
    
    def _get_books_from_search(self):
        """Lấy sách từ lịch sử tìm kiếm"""
        searches = list(SearchHistory.objects.filter(user=self.user).values_list('query', flat=True)[:10])
        
        if not searches:
            return []
        
        # Tìm sách dựa trên từ khóa tìm kiếm
        query = Q()
        for search_query in searches:
            query |= Q(title__icontains=search_query)
        
        return list(Book.objects.filter(query).distinct()[:10])
    
    def _get_popular_books(self, limit):
        """Lấy sách phổ biến"""
        return Book.objects.filter(
            quantity__gt=0
        ).order_by('-sold_quantity', '-quantity')[:limit]
    
    def get_similar_books(self, book, limit=6):
        """Lấy sách tương tự với một cuốn sách cụ thể"""
        categories = list(book.categories.all())
        authors = list(book.authors.all())
        
        if not categories and not authors:
            return []
        
        similar_qs = Book.objects.filter(
            Q(categories__in=categories) | 
            Q(authors__in=authors)
        ).exclude(
            id=book.id
        ).distinct().order_by('-sold_quantity')
        
        return list(similar_qs[:limit])
    
    def get_trending_books(self, limit=10):
        """Lấy sách đang thịnh hành (bán chạy gần đây)"""
        return Book.objects.filter(
            quantity__gt=0
        ).order_by('-sold_quantity')[:limit]
    
    def get_new_arrivals(self, limit=10):
        """Lấy sách mới về"""
        return Book.objects.filter(
            quantity__gt=0
        ).order_by('-published_year', '-id')[:limit]
