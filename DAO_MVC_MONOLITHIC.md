# Tài liệu Kiến trúc - DAO, MVC và Monolithic

## 1. DAO (Data Access Object) Pattern

### Định nghĩa

DAO là một design pattern dùng để tách biệt logic nghiệp vụ (business logic) khỏi logic truy cập dữ liệu (data access logic). DAO cung cấp một interface trừu tượng để tương tác với database mà không cần quan tâm đến chi tiết triển khai.

### Lợi ích

- **Tách biệt rõ ràng**: Logic nghiệp vụ không phụ thuộc vào cách dữ liệu được lưu trữ
- **Dễ bảo trì**: Thay đổi database không ảnh hưởng đến business logic
- **Tái sử dụng**: Các DAO có thể dùng ở nhiều nơi
- **Dễ test**: Có thể mock DAO khi test business logic

### Cấu trúc DAO trong dự án

```
Model (Data Structure)
    ↓
DAO (Data Access)
    ↓
Database
```

### Ví dụ trong dự án

#### Model (store/models/book_models.py)

```python
class Book(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    # ... các trường khác
```

#### DAO (store/controllers/BookDAO/book_dao.py)

```python
class BookDAO:
    @staticmethod
    def get_all_books():
        return Book.objects.all()

    @staticmethod
    def get_book_by_id(book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def create_book(book_data):
        return Book.objects.create(**book_data)

    @staticmethod
    def update_book(book_id, **kwargs):
        book = Book.objects.get(id=book_id)
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        book.save()
        return book
```

#### Sử dụng DAO trong View

```python
# KHÔNG TỐT - Gọi trực tiếp Model
def book_list_view(request):
    books = Book.objects.all()  # Hard coupling
    return render(request, 'books.html', {'books': books})

# TỐT - Gọi qua DAO
def book_list_view(request):
    books = BookDAO.get_all_books()  # Loose coupling
    return render(request, 'books.html', {'books': books})
```

### Các DAO trong dự án (22 DAOs)

1. **UserDAO**: User, Customer, Staff management
2. **BookDAO**: Book, Category, Author, Publisher
3. **OrderDAO**: Cart, Order, Payment, Voucher
4. **WarehouseDAO**: Warehouse, ImportSlip, Supplier
5. **ShippingDAO**: Shipping, Tracking

---

## 2. MVC (Model-View-Controller) Pattern

### Định nghĩa

MVC là mô hình kiến trúc phần mềm chia ứng dụng thành 3 thành phần chính:

- **Model**: Quản lý dữ liệu và business logic
- **View**: Hiển thị dữ liệu cho người dùng
- **Controller**: Xử lý input, điều phối giữa Model và View

### Lợi ích

- **Separation of Concerns**: Mỗi thành phần có trách nhiệm riêng
- **Song song phát triển**: Team có thể làm việc độc lập trên từng phần
- **Dễ maintain**: Thay đổi giao diện không ảnh hưởng logic
- **Reusable**: Model có thể dùng cho nhiều View

### MVC trong Django

Django sử dụng biến thể của MVC gọi là **MTV (Model-Template-View)**:

- **Model**: Giống MVC Model
- **Template**: Giống MVC View (hiển thị)
- **View**: Giống MVC Controller (logic xử lý)

### Cấu trúc MVC trong dự án

```
Request
    ↓
URLs (Routing)
    ↓
View (Controller) - Xử lý logic nghiệp vụ
    ↓
DAO - Truy cập dữ liệu
    ↓
Model - Cấu trúc dữ liệu
    ↓
Database
    ↑
View (Controller) - Chuẩn bị dữ liệu
    ↓
Template (View) - Hiển thị
    ↓
Response
```

### Ví dụ luồng MVC trong dự án

#### 1. Request đến (URLs)

```python
# store/urls.py
path('books/', views.book_list_view, name='book_list')
```

#### 2. Controller xử lý (View)

```python
# store/views/book_views.py
def book_list_view(request):
    # Lấy dữ liệu qua DAO
    books = BookDAO.get_all_books()
    categories = CategoryDAO.get_all_categories()

    # Filter nếu có
    category = request.GET.get('category')
    if category:
        books = BookDAO.get_books_by_category(category)

    # Chuẩn bị context
    context = {
        'books': books,
        'categories': categories
    }

    # Render template
    return render(request, 'books/book_list.html', context)
```

#### 3. Model (Dữ liệu)

```python
# store/models/book_models.py
class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # ...
```

#### 4. Template (Hiển thị)

```html
<!-- store/templates/books/book_list.html -->
{% for book in books %}
<div class="book">
  <h3>{{ book.title }}</h3>
  <p>Price: ${{ book.price }}</p>
</div>
{% endfor %}
```

---

## 3. Monolithic Architecture

### Định nghĩa

Monolithic là kiến trúc phần mềm truyền thống, nơi toàn bộ ứng dụng được xây dựng như một đơn vị duy nhất, không chia nhỏ thành các service riêng biệt.

### Đặc điểm Monolithic

#### Ưu điểm

1. **Đơn giản triển khai**: Một codebase, một deployment
2. **Dễ phát triển ban đầu**: Không cần setup phức tạp
3. **Performance tốt**: Không có network latency giữa các component
4. **Dễ debug**: Toàn bộ code ở một nơi
5. **Transaction đơn giản**: Chung database, dễ quản lý ACID

#### Nhược điểm

1. **Khó scale**: Phải scale toàn bộ app, không thể scale từng phần
2. **Deploy rủi ro**: Một thay đổi nhỏ phải deploy lại toàn bộ
3. **Technology lock-in**: Khó thay đổi công nghệ
4. **Codebase lớn**: Khó maintain khi project phát triển
5. **Thời gian build lâu**: Toàn bộ app phải compile lại

### Dự án Bookstore là Monolithic

#### Cấu trúc Monolithic của dự án

```
Bookstore Application (Monolithic)
├─ User Management
├─ Book Catalog
├─ Order Processing
├─ Warehouse Management
├─ Payment Processing
├─ Shipping & Tracking
├─ Recommendation Engine
└─ Admin Panel

↓ (Chung một database)
MySQL Database
```

#### Đặc điểm trong dự án

**1. Single Codebase**

```
bookstore03/
├─ models/       (Tất cả models)
├─ views/        (Tất cả views)
├─ controllers/  (Tất cả DAOs)
└─ services/     (Services)
```

**2. Single Database**

- Tất cả module dùng chung MySQL database
- Các bảng liên kết với nhau qua Foreign Key

**3. Single Deployment**

- Deploy toàn bộ ứng dụng cùng lúc
- Chạy trên một server/container

**4. Shared Resources**

- Chung authentication system
- Chung static files
- Chung configuration

#### Ví dụ tương tác giữa modules trong Monolithic

```python
# Đặt hàng (Order) cập nhật Sách (Book) và Kho (Warehouse)
def place_order(request):
    # Tạo order
    order = OrderDAO.create_order(customer, total)

    # Cập nhật sold quantity (Book module)
    for item in cart_items:
        BookDAO.update_sold_quantity(item.book.id, item.quantity)

    # Giảm tồn kho (Warehouse module)
    for item in cart_items:
        WarehouseDAO.decrease_stock(item.book.id, item.quantity)

    # Tạo payment (Payment module)
    PaymentDAO.create_payment(order, amount, method)

    # Tất cả trong một transaction
```

---

## 4. So sánh với Microservices

### Monolithic vs Microservices

| Tiêu chí      | Monolithic (Dự án hiện tại) | Microservices           |
| ------------- | --------------------------- | ----------------------- |
| Codebase      | Một codebase duy nhất       | Nhiều codebase độc lập  |
| Database      | Một database chung          | Mỗi service có DB riêng |
| Deployment    | Deploy toàn bộ              | Deploy từng service     |
| Scalability   | Scale toàn bộ app           | Scale từng service      |
| Technology    | Một stack công nghệ         | Đa dạng công nghệ       |
| Communication | Function calls              | HTTP/gRPC/Message Queue |
| Complexity    | Đơn giản hơn                | Phức tạp hơn            |

### Khi nào dùng Monolithic?

Dự án này phù hợp với Monolithic vì:

1. **Quy mô vừa phải**: Bookstore không cần scale cực lớn
2. **Team nhỏ**: Dễ quản lý một codebase
3. **Tight coupling**: Các module liên quan chặt chẽ (Order → Book → Warehouse)
4. **Development nhanh**: Không cần overhead của microservices
5. **Cost**: Ít resource hơn (1 server vs nhiều services)

---

## 5. Kết hợp DAO + MVC trong Monolithic

### Kiến trúc tổng thể của dự án

```
┌─────────────────── MONOLITHIC APPLICATION ───────────────────┐
│                                                                │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐            │
│  │  User    │      │  Book    │      │  Order   │            │
│  │  Module  │      │  Module  │      │  Module  │  ...       │
│  └──────────┘      └──────────┘      └──────────┘            │
│       │                  │                  │                 │
│       ├─ Views           ├─ Views           ├─ Views          │
│       ├─ DAOs            ├─ DAOs            ├─ DAOs           │
│       └─ Models          └─ Models          └─ Models         │
│                                                                │
│  ┌────────────────────────────────────────────────┐          │
│  │         Shared Database (MySQL)                 │          │
│  └────────────────────────────────────────────────┘          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Tầng trong kiến trúc

```
Presentation Layer (Templates)
    ↓
Controller Layer (Views)
    ↓
Service Layer (Recommendation Service, etc.)
    ↓
Data Access Layer (DAOs)
    ↓
Domain Layer (Models)
    ↓
Database Layer (MySQL)
```

### Lợi ích của cách tiếp cận này

1. **DAO Pattern**: Tách biệt data access
2. **MVC Pattern**: Tổ chức code rõ ràng
3. **Monolithic**: Đơn giản, phù hợp quy mô
4. **Layered Architecture**: Dễ maintain và mở rộng
5. **Single Responsibility**: Mỗi layer có nhiệm vụ riêng

---

## 6. Tóm tắt

### DAO trong dự án

- 22 DAOs xử lý tất cả data access
- Tách biệt hoàn toàn khỏi business logic
- Dễ test và maintain

### MVC trong dự án

- Models: 32 classes định nghĩa dữ liệu
- Views (Controllers): 64 views xử lý logic
- Templates: HTML hiển thị dữ liệu

### Monolithic trong dự án

- Single application
- Single database
- Single deployment
- Phù hợp với quy mô và yêu cầu

**Kết luận**: Dự án sử dụng kiến trúc Monolithic với DAO pattern và MVC pattern để tạo ra một hệ thống có cấu trúc rõ ràng, dễ maintain và phù hợp với yêu cầu của Bookstore Management System.
