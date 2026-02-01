from store.models import Wishlist


class WishlistDAO:
    
    @staticmethod
    def add_to_wishlist(customer, book):
        wishlist, created = Wishlist.objects.get_or_create(
            customer=customer,
            book=book
        )
        return wishlist, created
    
    @staticmethod
    def remove_from_wishlist(customer, book):
        try:
            wishlist = Wishlist.objects.get(customer=customer, book=book)
            wishlist.delete()
            return True
        except Wishlist.DoesNotExist:
            return False
    
    @staticmethod
    def get_customer_wishlist(customer):
        return customer.wishlists.all()
    
    @staticmethod
    def is_in_wishlist(customer, book):
        return Wishlist.objects.filter(customer=customer, book=book).exists()
    
    @staticmethod
    def clear_wishlist(customer):
        customer.wishlists.all().delete()
    
    @staticmethod
    def get_wishlist_count(customer):
        return customer.wishlists.count()
