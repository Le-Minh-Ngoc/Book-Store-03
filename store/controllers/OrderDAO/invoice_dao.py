from store.models import Invoice, InvoiceItem
from django.db import transaction
from decimal import Decimal


class InvoiceDAO:
    
    @staticmethod
    def create_invoice(order, voucher=None):
        with transaction.atomic():
            total = order.total
            discount = Decimal('0')
            
            if voucher:
                discount = (total * voucher.discount_percent) / 100
            
            final_amount = total - discount
            
            invoice = Invoice.objects.create(
                order=order,
                voucher=voucher,
                total=total,
                discount=discount,
                final_amount=final_amount
            )
            
            for order_item in order.items.all():
                InvoiceItem.objects.create(
                    invoice=invoice,
                    book=order_item.book,
                    quantity=order_item.quantity,
                    unit_price=order_item.price,
                    total_price=order_item.price * order_item.quantity
                )
            
            return invoice
    
    @staticmethod
    def get_invoice_by_id(invoice_id):
        try:
            return Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return None
    
    @staticmethod
    def get_order_invoice(order):
        if hasattr(order, 'invoice'):
            return order.invoice
        return None
    
    @staticmethod
    def get_all_invoices():
        return Invoice.objects.all()
    
    @staticmethod
    def get_invoice_items(invoice):
        return invoice.items.all()
    
    @staticmethod
    def calculate_invoice_total(invoice):
        return invoice.final_amount
    
    @staticmethod
    def delete_invoice(invoice_id):
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.delete()
