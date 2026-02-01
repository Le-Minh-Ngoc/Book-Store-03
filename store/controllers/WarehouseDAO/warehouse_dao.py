from store.models import Warehouse


class WarehouseDAO:
    
    @staticmethod
    def create_warehouse(name, location, capacity, manager=None):
        return Warehouse.objects.create(
            name=name,
            location=location,
            capacity=capacity,
            manager=manager
        )
    
    @staticmethod
    def get_warehouse_by_id(warehouse_id):
        try:
            return Warehouse.objects.get(id=warehouse_id)
        except Warehouse.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_warehouses():
        return Warehouse.objects.all()
    
    @staticmethod
    def update_warehouse(warehouse_id, **kwargs):
        warehouse = Warehouse.objects.get(id=warehouse_id)
        
        for key, value in kwargs.items():
            if hasattr(warehouse, key):
                setattr(warehouse, key, value)
        
        warehouse.save()
        return warehouse
    
    @staticmethod
    def delete_warehouse(warehouse_id):
        warehouse = Warehouse.objects.get(id=warehouse_id)
        warehouse.delete()
    
    @staticmethod
    def get_warehouse_import_slips(warehouse):
        return warehouse.import_slips.all()
    
    @staticmethod
    def assign_manager(warehouse, manager):
        warehouse.manager = manager
        warehouse.save()
        return warehouse
