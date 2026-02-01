from store.models import Cart, CartItem
from django.db import transaction


class CartDAO:
    
    @staticmethod
    def get_or_create_cart(customer):
        cart, created = Cart.objects.get_or_create(
            customer=customer,
            defaults={'id': f'CART-{customer.id}'}
        )
        return cart
    
    @staticmethod
    def get_cart_by_customer(customer):
        try:
            return Cart.objects.get(customer=customer)
        except Cart.DoesNotExist:
            return None
    
    @staticmethod
    def add_item(cart, book, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        CartDAO.update_total(cart)
        return cart_item
    
    @staticmethod
    def update_item_quantity(cart_item, quantity):
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        CartDAO.update_total(cart_item.cart)
    
    @staticmethod
    def remove_item(cart_item):
        cart = cart_item.cart
        cart_item.delete()
        CartDAO.update_total(cart)
    
    @staticmethod
    def update_total(cart):
        total = sum(item.book.price * item.quantity for item in cart.items.all())
        cart.total_price = total
        cart.save()
        return total
    
    @staticmethod
    def clear_cart(cart):
        cart.items.all().delete()
        cart.total_price = 0
        cart.save()
    
    @staticmethod
    def get_cart_items(cart):
        return cart.items.all()
    
    @staticmethod
    def get_cart_item_count(cart):
        return cart.items.count()
    
    @staticmethod
    def get_cart_total(cart):
        return cart.total_price
