from store.models import Payment, Transaction
import uuid


class PaymentDAO:
    
    @staticmethod
    def create_payment(order, amount, method, status='pending', payment_id=None):
        if payment_id is None:
            payment_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"
        
        payment = Payment.objects.create(
            id=payment_id,
            order=order,
            amount=amount,
            method=method,
            status=status
        )
        return payment
    
    @staticmethod
    def get_payment_by_id(payment_id):
        try:
            return Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return None
    
    @staticmethod
    def get_order_payment(order):
        if hasattr(order, 'payment'):
            return order.payment
        return None
    
    @staticmethod
    def update_payment_status(payment, status):
        payment.status = status
        payment.save()
        return payment
    
    @staticmethod
    def process_payment(payment):
        payment.status = 'completed'
        payment.save()
        return payment
    
    @staticmethod
    def get_all_payments():
        return Payment.objects.all()
    
    @staticmethod
    def get_payments_by_method(method):
        return Payment.objects.filter(method=method)
    
    @staticmethod
    def get_payments_by_status(status):
        return Payment.objects.filter(status=status)
    
    @staticmethod
    def create_transaction(payment, amount, status):
        transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
        
        transaction = Transaction.objects.create(
            payment=payment,
            transaction_id=transaction_id,
            amount=amount,
            status=status
        )
        return transaction
    
    @staticmethod
    def get_payment_transactions(payment):
        return payment.transactions.all()
