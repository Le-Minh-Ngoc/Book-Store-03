from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from store.models import Book
from store.services.recommendation_service import BookRecommendationService
from store.controllers.BookDAO.book_dao import BookDAO


def recommendations_view(request):
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
    book = BookDAO.get_book_by_id(book_id)
    if not book:
        return JsonResponse({'error': 'Book not found'}, status=404)
    
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
