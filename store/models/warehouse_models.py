from django.db import models
from .user_models import Supplier, Manager
from .book_models import Book


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    capacity = models.IntegerField()
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, related_name='warehouses')
    
    class Meta:
        db_table = 'warehouse'
    
    def __str__(self):
        return self.name


class ImportSlip(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='import_slips')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='import_slips')
    import_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, related_name='managed_imports')
    
    class Meta:
        db_table = 'import_slip'
        ordering = ['-import_date']
    
    def __str__(self):
        return f"Import {self.id}"


class ImportSlipDetail(models.Model):
    import_slip = models.ForeignKey(ImportSlip, on_delete=models.CASCADE, related_name='details')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='import_details')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        db_table = 'import_slip_detail'
