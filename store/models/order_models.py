from django.db import models
from .user_models import Customer, Shipper
from .book_models import Book


class Cart(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    class Meta:
        db_table = 'cart'
    
    def __str__(self):
        return f"Cart {self.id} - {self.customer}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'cart_item'
        unique_together = ('cart', 'book')


class Order(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'order'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'order_item'


class OrderStatus(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=50)
    note = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'order_status'
        ordering = ['-updated_at']


class Payment(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'payment'
    
    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'payment_method'
    
    def __str__(self):
        return self.name


class Voucher(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    min_order_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    class Meta:
        db_table = 'voucher'
    
    def __str__(self):
        return self.code


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'invoice'


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        db_table = 'invoice_item'


class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping')
    shipper = models.ForeignKey(Shipper, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments')
    tracking_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    shipped_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'shipping'
    
    def __str__(self):
        return f"Shipping {self.tracking_number}"


class ShippingAddress(models.Model):
    shipping = models.OneToOneField(Shipping, on_delete=models.CASCADE, related_name='address')
    recipient_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'shipping_address'


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds')
    reason = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50)
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'refund'
        ordering = ['-requested_at']


class Transaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'transaction'
        ordering = ['-created_at']


class Carrier(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    
    class Meta:
        db_table = 'carrier'
    
    def __str__(self):
        return self.name


class Tracking(models.Model):
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, related_name='tracking_history')
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    
    class Meta:
        db_table = 'tracking'
        ordering = ['-timestamp']
