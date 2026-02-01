from store.models import Order, OrderItem, OrderStatus
from django.db import transaction
import uuid


class OrderDAO:
    
    @staticmethod
    def create_order(customer, total, status='pending'):
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        order = Order.objects.create(
            id=order_id,
            customer=customer,
            total=total,
            status=status
        )
        return order
    
    @staticmethod
    def get_order_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None
    
    @staticmethod
    def get_customer_orders(customer):
        return customer.orders.all()
    
    @staticmethod
    def get_all_orders():
        return Order.objects.all()
    
    @staticmethod
    def add_order_item(order, book, quantity, price):
        return OrderItem.objects.create(
            order=order,
            book=book,
            quantity=quantity,
            price=price
        )
    
    @staticmethod
    def get_order_items(order):
        return order.items.all()
    
    @staticmethod
    def update_order_status(order, status, note=''):
        order.status = status
        order.save()
        
        OrderStatus.objects.create(
            order=order,
            status=status,
            note=note
        )
        
        return order
    
    @staticmethod
    def cancel_order(order):
        if order.status in ['pending', 'processing']:
            with transaction.atomic():
                for item in order.items.all():
                    item.book.quantity += item.quantity
                    item.book.sold_quantity -= item.quantity
                    item.book.save()
                
                OrderDAO.update_order_status(order, 'cancelled', 'Cancelled by customer')
                return True
        return False
    
    @staticmethod
    def get_orders_by_status(status):
        return Order.objects.filter(status=status)
    
    @staticmethod
    def get_order_status_history(order):
        return order.status_history.all()
    
    @staticmethod
    def delete_order(order_id):
        order = Order.objects.get(id=order_id)
        order.delete()
