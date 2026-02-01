# Bookstore Django Project - Cau truc MVC

Du an Django cho he thong quan ly cua hang sach voi cau truc MVC (Model-View-Controller).

## Cau truc du an

```
bookstore03/
├── bookstore03/              # Cau hinh du an chinh
│   ├── settings.py          # Cau hinh Django
│   ├── urls.py              # URL routing chinh
│   └── wsgi.py              # WSGI config
│
└── store/                    # App chinh (MVC)
    ├── models/              # MODELS - Lop du lieu
    │   ├── user_models.py   # Models cho User, Customer, Staff, etc.
    │   ├── book_models.py   # Models cho Book, Author, Publisher, etc.
    │   ├── order_models.py  # Models cho Order, Cart, Payment, etc.
    │   └── warehouse_models.py  # Models cho Warehouse, ImportSlip, etc.
    │
    ├── views/               # VIEWS - Lop giao dien
    │   ├── user_views.py    # Views cho authentication va user management
    │   ├── book_views.py    # Views cho book catalog va search
    │   ├── order_views.py   # Views cho cart va ordering
    │   └── warehouse_views.py  # Views cho warehouse management
    │
    ├── controllers/         # CONTROLLERS - Lop logic nghiep vu
    │   ├── user_controllers.py     # Business logic cho users
    │   ├── book_controllers.py     # Business logic cho books
    │   ├── order_controllers.py    # Business logic cho orders
    │   └── warehouse_controllers.py # Business logic cho warehouse
    │
    ├── templates/           # HTML templates
    ├── admin.py            # Django admin configuration
    └── urls.py             # URL routing cho store app

```

## Cac Models

### User Models (user_models.py)
- User: Nguoi dung he thong (ke thua AbstractUser)
- Customer: Khach hang
- Staff: Nhan vien
- Supplier: Nha cung cap
- MemberShip: Thanh vien
- Address: Dia chi
- LoginHistory: Lich su dang nhap
- SearchHistory: Lich su tim kiem
- Role: Vai tro
- Manager: Quan ly
- Admin: Quan tri vien
- Shipper: Nguoi giao hang
- Notification: Thong bao

### Book Models (book_models.py)
- Category: The loai sach
- Publisher: Nha xuat ban
- Author: Tac gia
- Book: Sach
- BookAuthor: Lien ket sach - tac gia
- BookCategory: Lien ket sach - the loai
- BookImage: Hinh anh sach
- Review: Danh gia
- Comment: Binh luan
- Wishlist: Danh sach yeu thich
- DamagedBook: Sach bi hong

### Order Models (order_models.py)
- Cart: Gio hang
- CartItem: San pham trong gio hang
- Order: Don hang
- OrderItem: San pham trong don hang
- OrderStatus: Trang thai don hang
- Payment: Thanh toan
- PaymentMethod: Phuong thuc thanh toan
- Voucher: Ma giam gia
- Invoice: Hoa don
- InvoiceItem: Chi tiet hoa don
- Shipping: Van chuyen
- ShippingAddress: Dia chi van chuyen
- Refund: Hoan tien
- Transaction: Giao dich
- Carrier: Don vi van chuyen
- Tracking: Theo doi van chuyen

### Warehouse Models (warehouse_models.py)
- Warehouse: Kho hang
- ImportSlip: Phieu nhap kho
- ImportSlipDetail: Chi tiet phieu nhap kho

## Cac Views

### User Views
- Dang ky, dang nhap, dang xuat
- Quan ly thong tin ca nhan
- Quan ly dia chi
- Xem thong bao
- Lich su dang nhap va tim kiem

### Book Views
- Danh sach sach
- Chi tiet sach
- Tim kiem sach
- Danh gia va binh luan
- Wishlist
- Danh sach tac gia, nha xuat ban, the loai

### Order Views
- Gio hang
- Checkout
- Dat hang
- Quan ly don hang
- Ap dung voucher
- Huy don hang

### Warehouse Views
- Quan ly kho
- Phieu nhap kho
- Ton kho

## Cac Controllers

### User Controllers
- UserController: Quan ly nguoi dung
- CustomerController: Quan ly khach hang
- StaffController: Quan ly nhan vien
- LoginHistoryController: Quan ly lich su dang nhap

### Book Controllers
- BookController: Quan ly sach
- CategoryController: Quan ly the loai
- AuthorController: Quan ly tac gia
- PublisherController: Quan ly nha xuat ban
- ReviewController: Quan ly danh gia
- WishlistController: Quan ly wishlist
- DamagedBookController: Quan ly sach hong

### Order Controllers
- CartController: Quan ly gio hang
- OrderController: Quan ly don hang
- PaymentController: Quan ly thanh toan
- InvoiceController: Quan ly hoa don
- VoucherController: Quan ly voucher
- ShippingController: Quan ly van chuyen

### Warehouse Controllers
- WarehouseController: Quan ly kho
- ImportSlipController: Quan ly phieu nhap
- SupplierController: Quan ly nha cung cap
- InventoryController: Quan ly ton kho

## Cai dat va Chay du an

1. Tao migration:
```bash
python manage.py makemigrations
```

2. Chay migration:
```bash
python manage.py migrate
```

3. Tao superuser:
```bash
python manage.py createsuperuser
```

4. Chay server:
```bash
python manage.py runserver
```

5. Truy cap:
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
