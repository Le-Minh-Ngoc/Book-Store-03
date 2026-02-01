# Hướng dẫn chụp 6 Screenshots Giao diện

## Assignment 03: Bookstore Management System

Theo yêu cầu Chương 4, cần chụp 6 ảnh màn hình giao diện:

---

## Screenshot 1: Nhân viên nhập sách

### URL để truy cập:

```
http://localhost:8000/import-slips/create/
```

### Yêu cầu:

- Đăng nhập với tài khoản Staff/Manager
- Hiển thị form tạo phiếu nhập kho mới
- Chọn nhà cung cấp
- Chọn kho hàng
- Thêm sách vào phiếu nhập

### Nội dung cần có trong screenshot:

- Form tạo import slip
- Dropdown chọn supplier
- Dropdown chọn warehouse
- Bảng danh sách sách cần nhập
- Số lượng và đơn giá
- Tổng giá trị phiếu nhập
- Nút Submit

### Lệnh chạy server (nếu chưa chạy):

```bash
python manage.py runserver
```

---

## Screenshot 2: Khách hàng tìm sách

### URL để truy cập:

```
http://localhost:8000/books/?search=python
```

### Yêu cầu:

- Đăng nhập với tài khoản Customer (hoặc không cần đăng nhập)
- Hiển thị trang danh sách sách
- Có thanh tìm kiếm
- Kết quả tìm kiếm hiển thị các sách phù hợp

### Nội dung cần có trong screenshot:

- Thanh search với từ khóa đã nhập
- Danh sách sách kết quả tìm kiếm
- Thông tin sách: hình ảnh, tiêu đề, tác giả, giá
- Filter theo category (nếu có)
- Sort options (nếu có)
- Số lượng kết quả tìm được

---

## Screenshot 3: Gợi ý sách

### URL để truy cập:

```
http://localhost:8000/recommendations/
```

### Yêu cầu:

- Đăng nhập với tài khoản Customer
- Hệ thống phân tích lịch sử và hiển thị sách gợi ý

### Nội dung cần có trong screenshot:

- Danh sách sách được gợi ý
- Phần "Recommended for You"
- Phần "Trending Books"
- Phần "New Arrivals"
- Thông tin sách: hình, tiêu đề, giá
- Nút "Add to Cart" hoặc "View Details"

---

## Screenshot 4: Tạo giỏ hàng

### URL để truy cập:

```
http://localhost:8000/cart/
```

### Yêu cầu:

- Đăng nhập với tài khoản Customer
- Đã thêm ít nhất 2-3 sách vào giỏ hàng
- Hiển thị giỏ hàng với các sách đã chọn

### Nội dung cần có trong screenshot:

- Danh sách sách trong giỏ
- Mỗi item có: hình ảnh, tên sách, giá, số lượng
- Nút tăng/giảm số lượng
- Nút xóa khỏi giỏ
- Tổng tiền tạm tính
- Nút "Proceed to Checkout"

### Cách thêm sách vào giỏ:

1. Vào trang books: `http://localhost:8000/books/`
2. Click vào một cuốn sách
3. Click nút "Add to Cart"
4. Lặp lại với 2-3 cuốn sách khác
5. Vào `http://localhost:8000/cart/` để chụp

---

## Screenshot 5: Thanh toán

### URL để truy cập:

```
http://localhost:8000/checkout/
```

### Yêu cầu:

- Đăng nhập với tài khoản Customer
- Có sách trong giỏ hàng
- Hiển thị trang checkout

### Nội dung cần có trong screenshot:

- Thông tin đơn hàng (sách, số lượng, giá)
- Form địa chỉ giao hàng
- Chọn phương thức thanh toán (Cash/Card/Bank Transfer)
- Ô nhập mã voucher (optional)
- Tổng tiền cuối cùng
- Nút "Place Order"

### Cách thực hiện:

1. Đảm bảo có sách trong cart
2. Vào cart: `http://localhost:8000/cart/`
3. Click "Checkout"
4. Điền thông tin địa chỉ (nếu chưa có)
5. Chụp màn hình checkout

---

## Screenshot 6: Shipping (Theo dõi vận chuyển)

### URL để truy cập:

```
http://localhost:8000/orders/<order_id>/track/
```

hoặc

```
http://localhost:8000/tracking/?tracking_number=TRK-XXXXXXXXXX
```

### Yêu cầu:

- Đăng nhập với tài khoản Customer
- Đã có đơn hàng với shipping
- Hiển thị trang tracking

### Nội dung cần có trong screenshot:

- Order ID hoặc Tracking Number
- Trạng thái đơn hàng hiện tại
- Lịch sử tracking (timeline):
  - Pending
  - Processing
  - Shipped
  - In Transit
  - Delivered
- Mỗi status có timestamp
- Thông tin shipper (nếu đã gán)
- Địa chỉ giao hàng
- Estimated delivery date (nếu có)

### Cách tạo dữ liệu để chụp:

#### Cách 1: Qua Django Admin

1. Truy cập: `http://localhost:8000/admin/`
2. Đăng nhập với superuser
3. Vào Shipping
4. Tạo hoặc chỉnh sửa một shipping record
5. Thêm tracking history
6. Back về customer view để chụp

#### Cách 2: Qua Admin Panel

1. Truy cập: `http://localhost:8000/admin-panel/shippings/`
2. Đăng nhập với admin
3. Chọn một shipping
4. Update status và thêm tracking
5. Đăng nhập lại bằng customer
6. Truy cập tracking page để chụp

---

## Checklist trước khi chụp

### Chuẩn bị dữ liệu:

- [ ] Tạo ít nhất 10-15 books
- [ ] Tạo 2-3 categories
- [ ] Tạo 1-2 suppliers
- [ ] Tạo 1 warehouse
- [ ] Tạo 1 customer account
- [ ] Tạo 1 staff account
- [ ] Tạo 1 admin account
- [ ] Tạo 1-2 import slips
- [ ] Customer đã search, thêm vào cart, đặt hàng
- [ ] Có ít nhất 1 order với shipping đã được tracking

### Chạy migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Tạo superuser (nếu chưa có):

```bash
python manage.py createsuperuser
```

### Chạy server:

```bash
python manage.py runserver
```

---

## Lưu ý khi chụp screenshots

1. **Chụp toàn màn hình** hoặc phần browser window
2. **URL phải hiển thị** trong thanh địa chỉ
3. **Dữ liệu phải thật**, không để trống
4. **Giao diện phải rõ ràng**, không bị lỗi hiển thị
5. **Chụp ở resolution phù hợp** (1920x1080 hoặc 1366x768)
6. **Format ảnh**: PNG hoặc JPG
7. **Đặt tên file rõ ràng**:
   - `screenshot_1_nhan_vien_nhap_sach.png`
   - `screenshot_2_khach_hang_tim_sach.png`
   - `screenshot_3_goi_y_sach.png`
   - `screenshot_4_gio_hang.png`
   - `screenshot_5_thanh_toan.png`
   - `screenshot_6_tracking_van_chuyen.png`

---

## Script tạo dữ liệu mẫu nhanh

Tạo file `create_sample_data.py` trong thư mục gốc:

```python
# Chạy: python manage.py shell < create_sample_data.py

from store.models import *
from store.controllers.BookDAO.book_dao import BookDAO
from store.controllers.UserDAO.userdao import UserDAO

# Tạo user mẫu
customer_user = UserDAO.create_user(
    username='customer1',
    email='customer@test.com',
    password='123456',
    fullname='Nguyen Van A'
)

# Tạo books mẫu
categories = ['Fiction', 'Technology', 'Business']
for cat_name in categories:
    Category.objects.create(type=cat_name)

books_data = [
    {'title': 'Python Programming', 'price': 29.99, 'quantity': 50},
    {'title': 'Django for Beginners', 'price': 39.99, 'quantity': 30},
    {'title': 'Data Science Handbook', 'price': 49.99, 'quantity': 20},
]

for book_data in books_data:
    BookDAO.create_book(book_data)

print("Sample data created successfully!")
```

---

## Tổng kết

Sau khi chụp xong 6 screenshots, lưu vào folder `screenshots/` trong thư mục dự án để nộp cùng assignment.
