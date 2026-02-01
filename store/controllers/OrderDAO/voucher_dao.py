from store.models import Voucher
from django.utils import timezone


class VoucherDAO:
    
    @staticmethod
    def create_voucher(voucher_data):
        return Voucher.objects.create(**voucher_data)
    
    @staticmethod
    def get_voucher_by_id(voucher_id):
        try:
            return Voucher.objects.get(id=voucher_id)
        except Voucher.DoesNotExist:
            return None
    
    @staticmethod
    def get_voucher_by_code(code):
        try:
            return Voucher.objects.get(code=code)
        except Voucher.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_vouchers():
        return Voucher.objects.all()
    
    @staticmethod
    def get_active_vouchers():
        today = timezone.now().date()
        return Voucher.objects.filter(
            start_date__lte=today,
            end_date__gte=today
        )
    
    @staticmethod
    def validate_voucher(code, order_total):
        try:
            voucher = Voucher.objects.get(code=code)
            today = timezone.now().date()
            
            if voucher.start_date <= today <= voucher.end_date:
                if order_total >= voucher.min_order_value:
                    return voucher, None
                else:
                    return None, f"Minimum order value is {voucher.min_order_value}"
            else:
                return None, "Voucher expired"
        except Voucher.DoesNotExist:
            return None, "Invalid voucher code"
    
    @staticmethod
    def apply_discount(order_total, voucher):
        from decimal import Decimal
        discount = (order_total * voucher.discount_percent) / 100
        return order_total - discount
    
    @staticmethod
    def update_voucher(voucher_id, **kwargs):
        voucher = Voucher.objects.get(id=voucher_id)
        
        for key, value in kwargs.items():
            if hasattr(voucher, key):
                setattr(voucher, key, value)
        
        voucher.save()
        return voucher
    
    @staticmethod
    def delete_voucher(voucher_id):
        voucher = Voucher.objects.get(id=voucher_id)
        voucher.delete()
    
    @staticmethod
    def is_valid(voucher):
        today = timezone.now().date()
        return voucher.start_date <= today <= voucher.end_date
