# Refactor Log - Bookstore Project

## Ngày thực hiện: 2026-02-01

## Mục tiêu

Refactor dự án để tuân thủ chuẩn kiến trúc MVC/DAO:

- Tách Views thành các module riêng biệt
- Views gọi qua DAOs thay vì trực tiếp truy cập Models
- Đảm bảo tách biệt rõ ràng giữa các layer

## Thay đổi chính

### 1. Cấu trúc Views

**Trước:**

- Một file lớn `store/views.py` (925 dòng)
- Views gọi trực tiếp Models (ví dụ: `Book.objects.all()`)

**Sau:**

- Tách thành thư mục `store/views/` với các module:
  - `user_views.py` - Xác thực và quản lý người dùng
  - `book_views.py` - Catalog và tìm kiếm sách
  - `order_views.py` - Giỏ hàng và đặt hàng
  - `warehouse_views.py` - Quản lý kho
  - `recommendation_views.py` - Gợi ý sách
  - `manager_views.py` - Dashboard quản lý
  - `__init__.py` - Import tất cả views

### 2. Sử dụng DAOs

**Trước:**

```python
# Gọi trực tiếp Model
books = Book.objects.all()
user = User.objects.get(id=user_id)
```

**Sau:**

```python
# Gọi qua DAO layer
books = BookDAO.get_all_books()
user = UserDAO.get_user_by_id(user_id)
```

### 3. Các DAOs đã sử dụng

#### User Layer

- `UserDAO` - Quản lý User
- `CustomerDAO` - Quản lý Customer
- `LoginHistoryDAO` - Lịch sử đăng nhập
- `SearchHistoryDAO` - Lịch sử tìm kiếm
- `NotificationDAO` - Thông báo

#### Book Layer

- `BookDAO` - Quản lý sách
- `CategoryDAO` - Quản lý thể loại
- `AuthorDAO` - Quản lý tác giả
- `PublisherDAO` - Quản lý nhà xuất bản
- `ReviewDAO` - Quản lý đánh giá
- `CommentDAO` - Quản lý bình luận
- `WishlistDAO` - Quản lý wishlist
- `DamagedBookDAO` - Quản lý sách hỏng

#### Order Layer

- `CartDAO` - Quản lý giỏ hàng
- `OrderDAO` - Quản lý đơn hàng
- `PaymentDAO` - Quản lý thanh toán
- `VoucherDAO` - Quản lý voucher

#### Warehouse Layer

- `WarehouseDAO` - Quản lý kho
- `ImportSlipDAO` - Quản lý phiếu nhập
- `SupplierDAO` - Quản lý nhà cung cấp

### 4. Các DAO đã được cải tiến

- `AuthorDAO.get_author_books()` - Hỗ trợ cả author object và author_id
- `PublisherDAO.get_publisher_books()` - Hỗ trợ cả publisher object và publisher_id
- `PaymentDAO.create_payment()` - Hỗ trợ payment_id tùy chọn
- `LoginHistoryDAO` - Thêm alias method `create_login_history()`
- `SearchHistoryDAO` - Thêm alias method `create_search_history()`
- `VoucherDAO` - Thêm method `is_voucher_valid()`

### 5. Files đã thay đổi

**Files mới:**

- `store/views/__init__.py`
- `store/views/user_views.py`
- `store/views/book_views.py`
- `store/views/order_views.py`
- `store/views/warehouse_views.py`
- `store/views/recommendation_views.py`
- `store/views/manager_views.py`

**Files đã sửa:**

- `STRUCTURE.md` - Cập nhật tài liệu cấu trúc
- `store/controllers/BookDAO/author_dao.py`
- `store/controllers/BookDAO/publisher_dao.py`
- `store/controllers/UserDAO/history_dao.py`
- `store/controllers/OrderDAO/payment_dao.py`
- `store/controllers/OrderDAO/voucher_dao.py`

**Files backup:**

- `store/views.py` → `store/views_old.py`

### 6. Lợi ích đạt được

1. **Tách biệt rõ ràng giữa các layer:**
   - Views chỉ xử lý request/response
   - DAOs xử lý truy cập database
   - Models chỉ định nghĩa cấu trúc dữ liệu

2. **Dễ bảo trì:**
   - Mỗi file nhỏ, tập trung vào một chức năng
   - Dễ tìm và sửa lỗi
   - Dễ thêm tính năng mới

3. **Tái sử dụng code:**
   - DAOs có thể dùng ở nhiều nơi
   - Giảm duplicate code

4. **Testable:**
   - Dễ viết unit test cho từng layer
   - Có thể mock DAOs khi test Views

## Checklist kiểm tra

- [x] Tách Views thành các module riêng
- [x] Views gọi qua DAOs
- [x] Cập nhật STRUCTURE.md
- [x] Backup file views.py cũ
- [x] Đảm bảo import đúng trong **init**.py
- [x] URL routing vẫn hoạt động (không cần sửa urls.py)

## Lưu ý tiếp theo

1. Test lại toàn bộ chức năng để đảm bảo không có lỗi
2. Có thể xóa file `views_old.py` sau khi test xong
3. Nếu có lỗi import, kiểm tra lại **init**.py

## Kiến trúc sau khi refactor

```
Request → URL Router → View (logic hiển thị) → DAO (truy cập DB) → Model (định nghĩa dữ liệu) → Database
                         ↑
                    Service Layer (logic phức tạp như recommendation)
```
