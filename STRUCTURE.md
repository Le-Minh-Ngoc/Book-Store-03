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
    ├── views/               # VIEWS - Lop giao dien (da duoc tach)
    │   ├── user_views.py    # Views cho authentication va user management
    │   ├── book_views.py    # Views cho book catalog va search
    │   ├── order_views.py   # Views cho cart va ordering
    │   ├── warehouse_views.py  # Views cho warehouse management
    │   ├── recommendation_views.py  # Views cho recommendation
    │   └── manager_views.py  # Views cho manager dashboard
    ├── services/            # SERVICES - Cac logic phuc tap (Recommendation, etc.)
    │
    ├── controllers/         # DAOs & CONTROLLERS - Lop truy xuat du lieu
    │   ├── UserDAO/         # DAOs cho users (user_dao.py, etc.)
    │   ├── BookDAO/         # DAOs cho books (book_dao.py, author_dao.py...)
    │   ├── OrderDAO/        # DAOs cho orders (order_dao.py, cart_dao.py...)
    │   ├── CartDAO/         # DAOs cho cart
    │   └── WarehouseDAO/    # DAOs cho warehouse
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

## Cac Views (da duoc tach thanh cac module rieng biet)

### User Views (store/views/user_views.py)

- Dang ky, dang nhap, dang xuat (su dung UserDAO, CustomerDAO)
- Quan ly thong tin ca nhan (su dung UserDAO)
- Quan ly dia chi (su dung CustomerDAO)
- Xem thong bao (su dung NotificationDAO)
- Lich su dang nhap va tim kiem (su dung LoginHistoryDAO, SearchHistoryDAO)

### Book Views (store/views/book_views.py)

- Danh sach sach (su dung BookDAO, CategoryDAO)
- Chi tiet sach (su dung BookDAO, ReviewDAO, CommentDAO)
- Tim kiem sach (su dung BookDAO, SearchHistoryDAO)
- Danh gia va binh luan (su dung ReviewDAO, CommentDAO)
- Wishlist (su dung WishlistDAO)
- Danh sach tac gia, nha xuat ban, the loai (su dung AuthorDAO, PublisherDAO, CategoryDAO)

### Order Views (store/views/order_views.py)

- Gio hang (su dung CartDAO)
- Checkout (su dung CartDAO, CustomerDAO)
- Dat hang (su dung OrderDAO, CartDAO, BookDAO, PaymentDAO)
- Quan ly don hang (su dung OrderDAO)
- Ap dung voucher (su dung VoucherDAO)
- Huy don hang (su dung OrderDAO)

### Warehouse Views (store/views/warehouse_views.py)

- Quan ly kho (su dung WarehouseDAO)
- Phieu nhap kho (su dung ImportSlipDAO)
- Ton kho (su dung BookDAO)

### Manager Views (store/views/manager_views.py)

- Dashboard (su dung BookDAO, DamagedBookDAO)
- Quan ly sach (su dung BookDAO, CategoryDAO)
- Kiem tra ton kho (su dung BookDAO)
- Quan ly sach hong (su dung DamagedBookDAO)

### Recommendation Views (store/views/recommendation_views.py)

- Goi y sach (su dung BookRecommendationService)

## Cac Controllers & DAOs

(Hien tai du an dang trien khai theo mo hinh DAO pattern trong thu muc controllers)

### User DAOs (store/controllers/UserDAO)

- UserDAO: Truu tuong hoa truy xuat User
- CustomerDAO, StaffDAO...

### Book DAOs (store/controllers/BookDAO)

- BookDAO: Quan ly truy xuat sach
- CategoryDAO, AuthorDAO, PublisherDAO...

### Order DAOs (store/controllers/OrderDAO)

- CartDAO: Quan ly gio hang
- OrderDAO: Quan ly don hang
- PaymentDAO...

### Warehouse DAOs (store/controllers/WarehouseDAO)

- WarehouseDAO
- ImportSlipDAO...

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
