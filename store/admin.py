from django.contrib import admin
from store.models import (
    User, Customer, Staff, Supplier, MemberShip, Address,
    LoginHistory, SearchHistory, Role, Manager, Admin as AdminModel,
    Shipper, Notification, Category, Publisher, Author, Book,
    BookAuthor, BookCategory, BookImage, Review, Comment, Wishlist,
    DamagedBook, Cart, CartItem, Order, OrderItem, OrderStatus,
    Payment, PaymentMethod, Voucher, Invoice, InvoiceItem,
    Shipping, ShippingAddress, Refund, Transaction, Carrier,
    Tracking, Warehouse, ImportSlip, ImportSlipDetail
)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'fullname', 'is_staff_member', 'date_joined')
    list_filter = ('is_staff_member', 'is_active')
    search_fields = ('username', 'email', 'fullname')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'tel')
    search_fields = ('user__username', 'user__email')


class StaffAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'quantity', 'sold_quantity', 'publisher')
    list_filter = ('publisher', 'language', 'published_year')
    search_fields = ('title', 'ISBN', 'description')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    search_fields = ('type',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'birthdate')
    list_filter = ('country',)
    search_fields = ('name',)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'customer__user__username')
    date_hierarchy = 'created_at'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'price')
    search_fields = ('order__id', 'book__title')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'method', 'status', 'payment_date')
    list_filter = ('method', 'status')
    search_fields = ('id', 'order__id')


class VoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'start_date', 'end_date', 'min_order_value')
    list_filter = ('start_date', 'end_date')
    search_fields = ('code',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price')
    search_fields = ('customer__user__username',)


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'manager')
    search_fields = ('name', 'location')


class ImportSlipAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'warehouse', 'import_date', 'total')
    list_filter = ('import_date',)
    search_fields = ('id', 'supplier__name')
    date_hierarchy = 'import_date'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'book', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'customer__user__username')


admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Supplier)
admin.site.register(MemberShip)
admin.site.register(Address)
admin.site.register(LoginHistory)
admin.site.register(SearchHistory)
admin.site.register(Role)
admin.site.register(Manager)
admin.site.register(AdminModel)
admin.site.register(Shipper)
admin.site.register(Notification)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthor)
admin.site.register(BookCategory)
admin.site.register(BookImage)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment)
admin.site.register(Wishlist)
admin.site.register(DamagedBook)

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderStatus)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentMethod)
admin.site.register(Voucher, VoucherAdmin)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Shipping)
admin.site.register(ShippingAddress)
admin.site.register(Refund)
admin.site.register(Transaction)
admin.site.register(Carrier)
admin.site.register(Tracking)

admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(ImportSlip, ImportSlipAdmin)
admin.site.register(ImportSlipDetail)
