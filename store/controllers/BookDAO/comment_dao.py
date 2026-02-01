from store.models import Comment


class CommentDAO:
    
    @staticmethod
    def create_comment(customer, book, content):
        return Comment.objects.create(
            customer=customer,
            book=book,
            content=content
        )
    
    @staticmethod
    def get_comment_by_id(comment_id):
        try:
            return Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return None
    
    @staticmethod
    def get_book_comments(book):
        return book.comments.all()
    
    @staticmethod
    def get_customer_comments(customer):
        return customer.comments.all()
    
    @staticmethod
    def update_comment(comment_id, content):
        comment = Comment.objects.get(id=comment_id)
        comment.content = content
        comment.save()
        return comment
    
    @staticmethod
    def delete_comment(comment_id):
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
    
    @staticmethod
    def get_recent_comments(limit=10):
        return Comment.objects.all()[:limit]
