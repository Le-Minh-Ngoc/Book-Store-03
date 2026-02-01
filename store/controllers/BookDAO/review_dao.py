from store.models import Review
from django.db.models import Avg


class ReviewDAO:
    
    @staticmethod
    def create_review(customer, book, rating, comment=''):
        return Review.objects.create(
            customer=customer,
            book=book,
            rating=rating,
            comment=comment
        )
    
    @staticmethod
    def get_review_by_id(review_id):
        try:
            return Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return None
    
    @staticmethod
    def get_book_reviews(book):
        return book.reviews.all()
    
    @staticmethod
    def get_customer_reviews(customer):
        return customer.reviews.all()
    
    @staticmethod
    def get_average_rating(book):
        avg = book.reviews.aggregate(Avg('rating'))
        return avg['rating__avg']
    
    @staticmethod
    def update_review(review_id, rating=None, comment=None):
        review = Review.objects.get(id=review_id)
        
        if rating is not None:
            review.rating = rating
        if comment is not None:
            review.comment = comment
        
        review.save()
        return review
    
    @staticmethod
    def delete_review(review_id):
        review = Review.objects.get(id=review_id)
        review.delete()
    
    @staticmethod
    def customer_has_reviewed(customer, book):
        return Review.objects.filter(customer=customer, book=book).exists()
    
    @staticmethod
    def get_recent_reviews(limit=10):
        return Review.objects.all()[:limit]
    
    @staticmethod
    def get_reviews_by_rating(rating):
        return Review.objects.filter(rating=rating)
