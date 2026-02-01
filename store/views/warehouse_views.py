from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models import Supplier, Warehouse
from store.controllers.WarehouseDAO.warehouse_dao import WarehouseDAO
from store.controllers.WarehouseDAO.import_slip_dao import ImportSlipDAO
from store.controllers.WarehouseDAO.supplier_dao import SupplierDAO
from store.controllers.BookDAO.book_dao import BookDAO


@login_required
def warehouse_list_view(request):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    warehouses = WarehouseDAO.get_all_warehouses()
    return render(request, 'warehouse/warehouse_list.html', {'warehouses': warehouses})


@login_required
def warehouse_detail_view(request, warehouse_id):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    warehouse = WarehouseDAO.get_warehouse_by_id(warehouse_id)
    if not warehouse:
        return JsonResponse({'error': 'Warehouse not found'}, status=404)
    
    import_slips = WarehouseDAO.get_warehouse_import_slips(warehouse)
    
    context = {
        'warehouse': warehouse,
        'import_slips': import_slips
    }
    
    return render(request, 'warehouse/warehouse_detail.html', context)


@login_required
def import_slip_list_view(request):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    import_slips = ImportSlipDAO.get_all_import_slips()
    return render(request, 'warehouse/import_slip_list.html', {'import_slips': import_slips})


@login_required
def import_slip_detail_view(request, slip_id):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    import_slip = ImportSlipDAO.get_import_slip_by_id(slip_id)
    if not import_slip:
        return JsonResponse({'error': 'Import slip not found'}, status=404)
    
    details = ImportSlipDAO.get_slip_details(import_slip)
    
    context = {
        'import_slip': import_slip,
        'details': details
    }
    
    return render(request, 'warehouse/import_slip_detail.html', context)


@login_required
def create_import_slip_view(request):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')
        warehouse_id = request.POST.get('warehouse_id')
        
        supplier = SupplierDAO.get_supplier_by_id(supplier_id)
        warehouse = WarehouseDAO.get_warehouse_by_id(warehouse_id)
        
        if not supplier or not warehouse:
            return JsonResponse({'error': 'Supplier or Warehouse not found'}, status=404)
        
        manager = None
        if hasattr(request.user.staff_profile, 'manager_profile'):
            manager = request.user.staff_profile.manager_profile
        
        import_slip = ImportSlipDAO.create_import_slip(
            supplier=supplier,
            warehouse=warehouse,
            manager=manager
        )
        
        return redirect('import_slip_detail', slip_id=import_slip.id)
    
    suppliers = SupplierDAO.get_all_suppliers()
    warehouses = WarehouseDAO.get_all_warehouses()
    
    context = {
        'suppliers': suppliers,
        'warehouses': warehouses
    }
    
    return render(request, 'warehouse/create_import_slip.html', context)


@login_required
def add_import_detail(request, slip_id):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        import_slip = ImportSlipDAO.get_import_slip_by_id(slip_id)
        if not import_slip:
            return JsonResponse({'error': 'Import slip not found'}, status=404)
        
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        
        book = BookDAO.get_book_by_id(book_id)
        if not book:
            return JsonResponse({'error': 'Book not found'}, status=404)
        
        ImportSlipDAO.add_detail(import_slip, book, quantity, price)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def inventory_view(request):
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    books = BookDAO.get_all_books().order_by('title')
    
    search = request.GET.get('search')
    if search:
        books = BookDAO.search_books(search)
    
    low_stock = request.GET.get('low_stock')
    if low_stock:
        books = books.filter(quantity__lt=10)
    
    context = {
        'books': books
    }
    
    return render(request, 'warehouse/inventory.html', context)
