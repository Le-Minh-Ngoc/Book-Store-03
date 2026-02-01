from django.urls import path
from store import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    path('profile/address/add/', views.add_address_view, name='add_address'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('login-history/', views.login_history_view, name='login_history'),
    path('search-history/', views.search_history_view, name='search_history'),
    
    path('books/', views.book_list_view, name='book_list'),
    path('books/<str:book_id>/', views.book_detail_view, name='book_detail'),
    path('books/<str:book_id>/review/', views.add_review, name='add_review'),
    path('books/<str:book_id>/comment/', views.add_comment, name='add_comment'),
    path('books/<str:book_id>/wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('categories/', views.category_list_view, name='category_list'),
    path('authors/', views.author_list_view, name='author_list'),
    path('authors/<str:author_id>/', views.author_detail_view, name='author_detail'),
    path('publishers/', views.publisher_list_view, name='publisher_list'),
    path('publishers/<str:publisher_id>/', views.publisher_detail_view, name='publisher_detail'),
    
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<str:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/item/<int:item_id>/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/item/<int:item_id>/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/place/', views.place_order, name='place_order'),
    path('orders/', views.order_list_view, name='order_list'),
    path('orders/<str:order_id>/', views.order_detail_view, name='order_detail'),
    path('orders/<str:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('orders/<str:order_id>/track/', views.track_order_view, name='track_order'),
    path('tracking/', views.track_by_number_view, name='track_by_number'),
    path('voucher/apply/', views.apply_voucher, name='apply_voucher'),
    
    path('warehouse/', views.warehouse_list_view, name='warehouse_list'),
    path('warehouse/<int:warehouse_id>/', views.warehouse_detail_view, name='warehouse_detail'),
    path('import-slips/', views.import_slip_list_view, name='import_slip_list'),
    path('import-slips/<str:slip_id>/', views.import_slip_detail_view, name='import_slip_detail'),
    path('import-slips/create/', views.create_import_slip_view, name='create_import_slip'),
    path('import-slips/<str:slip_id>/add-detail/', views.add_import_detail, name='add_import_detail'),
    path('inventory/', views.inventory_view, name='inventory'),
    
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('api/books/<str:book_id>/similar/', views.get_similar_books_api, name='similar_books_api'),
    
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/books/', views.manager_books_view, name='manager_books'),
    path('manager/inventory/', views.manager_inventory_view, name='manager_inventory'),
    path('manager/damaged-books/', views.manager_damaged_books_view, name='manager_damaged_books'),
    path('manager/books/add/', views.manager_add_book_view, name='manager_add_book'),
    path('manager/books/<str:book_id>/edit/', views.manager_edit_book_view, name='manager_edit_book'),
    path('manager/books/<str:book_id>/delete/', views.manager_delete_book_view, name='manager_delete_book'),
    
    # Admin URLs
    path('admin-panel/users/', views.admin_users_list_view, name='admin_users_list'),
    path('admin-panel/users/<int:user_id>/', views.admin_user_detail_view, name='admin_user_detail'),
    path('admin-panel/users/<int:user_id>/toggle-status/', views.admin_toggle_user_status, name='admin_toggle_user_status'),
    path('admin-panel/staff/create/', views.admin_create_staff_view, name='admin_create_staff'),
    
    path('admin-panel/orders/', views.admin_orders_list_view, name='admin_orders_list'),
    path('admin-panel/orders/<str:order_id>/', views.admin_order_detail_view, name='admin_order_detail'),
    path('admin-panel/orders/<str:order_id>/update-status/', views.admin_update_order_status, name='admin_update_order_status'),
    
    path('admin-panel/payments/', views.admin_payments_list_view, name='admin_payments_list'),
    path('admin-panel/payments/<str:payment_id>/update-status/', views.admin_update_payment_status, name='admin_update_payment_status'),
    
    path('admin-panel/shippings/', views.admin_shippings_list_view, name='admin_shippings_list'),
    path('admin-panel/shippings/<int:shipping_id>/', views.admin_shipping_detail_view, name='admin_shipping_detail'),
    path('admin-panel/shippings/<int:shipping_id>/update-status/', views.admin_update_shipping_status, name='admin_update_shipping_status'),
    path('admin-panel/shippings/<int:shipping_id>/assign-shipper/', views.admin_assign_shipper, name='admin_assign_shipper'),
]
