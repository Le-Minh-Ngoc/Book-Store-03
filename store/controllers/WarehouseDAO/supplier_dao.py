from store.models import Supplier


class SupplierDAO:
    
    @staticmethod
    def create_supplier(supplier_data):
        return Supplier.objects.create(**supplier_data)
    
    @staticmethod
    def get_supplier_by_id(supplier_id):
        try:
            return Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_suppliers():
        return Supplier.objects.all()
    
    @staticmethod
    def search_suppliers(name):
        return Supplier.objects.filter(name__icontains=name)
    
    @staticmethod
    def update_supplier(supplier_id, **kwargs):
        supplier = Supplier.objects.get(id=supplier_id)
        
        for key, value in kwargs.items():
            if hasattr(supplier, key):
                setattr(supplier, key, value)
        
        supplier.save()
        return supplier
    
    @staticmethod
    def delete_supplier(supplier_id):
        supplier = Supplier.objects.get(id=supplier_id)
        supplier.delete()
    
    @staticmethod
    def get_supplier_import_slips(supplier):
        return supplier.import_slips.all()
    
    @staticmethod
    def supplier_exists(supplier_id):
        return Supplier.objects.filter(id=supplier_id).exists()
