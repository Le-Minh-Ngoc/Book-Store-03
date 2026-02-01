from store.models import ImportSlip, ImportSlipDetail
from django.db import transaction
import uuid


class ImportSlipDAO:
    
    @staticmethod
    def create_import_slip(supplier, warehouse, manager=None):
        slip_id = f"IMP-{uuid.uuid4().hex[:8].upper()}"
        
        import_slip = ImportSlip.objects.create(
            id=slip_id,
            supplier=supplier,
            warehouse=warehouse,
            manager=manager,
            total=0
        )
        
        return import_slip
    
    @staticmethod
    def get_import_slip_by_id(slip_id):
        try:
            return ImportSlip.objects.get(id=slip_id)
        except ImportSlip.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_import_slips():
        return ImportSlip.objects.all()
    
    @staticmethod
    def get_warehouse_import_slips(warehouse):
        return warehouse.import_slips.all()
    
    @staticmethod
    def get_supplier_import_slips(supplier):
        return supplier.import_slips.all()
    
    @staticmethod
    def add_detail(import_slip, book, quantity, price):
        with transaction.atomic():
            total = quantity * price
            
            detail = ImportSlipDetail.objects.create(
                import_slip=import_slip,
                book=book,
                quantity=quantity,
                price=price,
                total=total
            )
            
            book.quantity += quantity
            book.save()
            
            ImportSlipDAO.calculate_total(import_slip)
            
            return detail
    
    @staticmethod
    def get_slip_details(import_slip):
        return import_slip.details.all()
    
    @staticmethod
    def calculate_total(import_slip):
        total = sum(detail.total for detail in import_slip.details.all())
        import_slip.total = total
        import_slip.save()
        return total
    
    @staticmethod
    def delete_import_slip(slip_id):
        import_slip = ImportSlip.objects.get(id=slip_id)
        import_slip.delete()
