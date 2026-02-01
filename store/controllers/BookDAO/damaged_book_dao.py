from store.models import DamagedBook


class DamagedBookDAO:
    
    @staticmethod
    def report_damaged_book(book, quantity, reason):
        return DamagedBook.objects.create(
            book=book,
            quantity=quantity,
            reason=reason,
            status='reported'
        )
    
    @staticmethod
    def get_damaged_book_by_id(damaged_id):
        try:
            return DamagedBook.objects.get(id=damaged_id)
        except DamagedBook.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_damaged_books():
        return DamagedBook.objects.all()
    
    @staticmethod
    def get_damaged_by_book(book):
        return book.damaged_records.all()
    
    @staticmethod
    def get_damaged_by_status(status):
        return DamagedBook.objects.filter(status=status)
    
    @staticmethod
    def update_status(damaged_id, status):
        damaged_book = DamagedBook.objects.get(id=damaged_id)
        damaged_book.status = status
        damaged_book.save()
        return damaged_book
    
    @staticmethod
    def delete_damaged_record(damaged_id):
        damaged_book = DamagedBook.objects.get(id=damaged_id)
        damaged_book.delete()
    
    @staticmethod
    def get_total_damaged_quantity():
        from django.db.models import Sum
        result = DamagedBook.objects.aggregate(total=Sum('quantity'))
        return result['total'] or 0
