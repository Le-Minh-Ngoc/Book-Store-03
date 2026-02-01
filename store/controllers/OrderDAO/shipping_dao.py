from store.models import Shipping, ShippingAddress, Tracking
from django.db import transaction
import uuid


class ShippingDAO:
    
    @staticmethod
    def create_shipping(order, shipper=None, status='pending'):
        tracking_number = f"TRK-{uuid.uuid4().hex[:10].upper()}"
        
        shipping = Shipping.objects.create(
            order=order,
            shipper=shipper,
            tracking_number=tracking_number,
            status=status
        )
        return shipping
    
    @staticmethod
    def get_shipping_by_id(shipping_id):
        try:
            return Shipping.objects.get(id=shipping_id)
        except Shipping.DoesNotExist:
            return None
    
    @staticmethod
    def get_shipping_by_tracking(tracking_number):
        try:
            return Shipping.objects.get(tracking_number=tracking_number)
        except Shipping.DoesNotExist:
            return None
    
    @staticmethod
    def get_order_shipping(order):
        if hasattr(order, 'shipping'):
            return order.shipping
        return None
    
    @staticmethod
    def get_all_shippings():
        return Shipping.objects.all()
    
    @staticmethod
    def get_shippings_by_status(status):
        return Shipping.objects.filter(status=status)
    
    @staticmethod
    def get_shipper_deliveries(shipper):
        return shipper.shipments.all()
    
    @staticmethod
    def update_shipping_status(shipping, status):
        shipping.status = status
        shipping.save()
        
        Tracking.objects.create(
            shipping=shipping,
            location='Warehouse',
            status=status
        )
        
        return shipping
    
    @staticmethod
    def assign_shipper(shipping, shipper):
        shipping.shipper = shipper
        shipping.save()
        return shipping
    
    @staticmethod
    def mark_as_shipped(shipping):
        from django.utils import timezone
        shipping.shipped_date = timezone.now()
        shipping.status = 'shipped'
        shipping.save()
        return shipping
    
    @staticmethod
    def mark_as_delivered(shipping):
        from django.utils import timezone
        shipping.delivered_date = timezone.now()
        shipping.status = 'delivered'
        shipping.save()
        return shipping
    
    @staticmethod
    def create_shipping_address(shipping, address_data):
        return ShippingAddress.objects.create(
            shipping=shipping,
            **address_data
        )
    
    @staticmethod
    def get_shipping_address(shipping):
        if hasattr(shipping, 'address'):
            return shipping.address
        return None
    
    @staticmethod
    def add_tracking(shipping, location, status, note=''):
        return Tracking.objects.create(
            shipping=shipping,
            location=location,
            status=status,
            note=note
        )
    
    @staticmethod
    def get_tracking_history(shipping):
        return shipping.tracking_history.all()
