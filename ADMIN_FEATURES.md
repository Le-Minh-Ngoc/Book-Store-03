# Các chức năng Admin đã thêm

## Ngày: 2026-02-02

## Tổng quan

Đã bổ sung đầy đủ các chức năng quản trị admin cho hệ thống, bao gồm quản lý người dùng, đơn hàng, thanh toán và vận chuyển.

## Chi tiết các views đã thêm

### 1. Quản lý Người dùng

#### `admin_users_list_view`

- URL: `/admin-panel/users/`
- Chức năng: Xem danh sách tất cả người dùng
- Filter: Theo role (customer/staff/admin), tìm kiếm theo username/email/fullname
- DAO sử dụng: `UserDAO`

#### `admin_user_detail_view`

- URL: `/admin-panel/users/<user_id>/`
- Chức năng: Xem chi tiết người dùng, lịch sử đơn hàng
- DAO sử dụng: `UserDAO`

#### `admin_toggle_user_status`

- URL: `/admin-panel/users/<user_id>/toggle-status/`
- Chức năng: Kích hoạt/vô hiệu hóa tài khoản người dùng
- DAO sử dụng: `UserDAO`

#### `admin_create_staff_view`

- URL: `/admin-panel/staff/create/`
- Chức năng: Tạo tài khoản nhân viên mới
- DAO sử dụng: `UserDAO`, `StaffDAO`

### 2. Quản lý Đơn hàng

#### `admin_orders_list_view`

- URL: `/admin-panel/orders/`
- Chức năng: Xem danh sách tất cả đơn hàng
- Filter: Theo status, tìm kiếm theo order ID/username
- Thống kê: Tổng doanh thu từ đơn hàng hoàn thành
- DAO sử dụng: `OrderDAO`

#### `admin_order_detail_view`

- URL: `/admin-panel/orders/<order_id>/`
- Chức năng: Xem chi tiết đơn hàng, items, payment, shipping, tracking
- DAO sử dụng: `OrderDAO`, `ShippingDAO`

#### `admin_update_order_status`

- URL: `/admin-panel/orders/<order_id>/update-status/`
- Chức năng: Cập nhật trạng thái đơn hàng
- Logic: Tự động tạo OrderStatus record
- DAO sử dụng: `OrderDAO`

### 3. Quản lý Thanh toán

#### `admin_payments_list_view`

- URL: `/admin-panel/payments/`
- Chức năng: Xem danh sách tất cả thanh toán
- Filter: Theo status (pending/completed/failed/refunded), method (cash/card/bank_transfer/e_wallet)
- Thống kê: Tổng số tiền đã thanh toán
- DAO sử dụng: `PaymentDAO`

#### `admin_update_payment_status`

- URL: `/admin-panel/payments/<payment_id>/update-status/`
- Chức năng: Cập nhật trạng thái thanh toán
- Logic tự động:
  - Nếu payment = 'completed' → Order status = 'processing'
- DAO sử dụng: `PaymentDAO`, `OrderDAO`

### 4. Quản lý Vận chuyển

#### `admin_shippings_list_view`

- URL: `/admin-panel/shippings/`
- Chức năng: Xem danh sách tất cả đơn vận chuyển
- Filter: Theo status (pending/assigned/picked_up/in_transit/shipped/delivered/failed)
- DAO sử dụng: `ShippingDAO`, `StaffDAO`

#### `admin_shipping_detail_view`

- URL: `/admin-panel/shippings/<shipping_id>/`
- Chức năng: Xem chi tiết vận chuyển, tracking history
- DAO sử dụng: `ShippingDAO`, `StaffDAO`

#### `admin_update_shipping_status`

- URL: `/admin-panel/shippings/<shipping_id>/update-status/`
- Chức năng: Cập nhật trạng thái vận chuyển
- Logic tự động:
  - Tạo Tracking record mới
  - Nếu shipping = 'delivered' → Order status = 'completed'
- DAO sử dụng: `ShippingDAO`, `OrderDAO`

#### `admin_assign_shipper`

- URL: `/admin-panel/shippings/<shipping_id>/assign-shipper/`
- Chức năng: Gán shipper cho đơn hàng
- Logic: Update shipping status = 'assigned'
- DAO sử dụng: `ShippingDAO`

## Quyền truy cập

### `check_admin_permission(user)`

Kiểm tra quyền admin bằng cách:

1. Kiểm tra `is_superuser`
2. Kiểm tra có `admin_profile` hoặc `manager_profile`

Tất cả views admin đều yêu cầu quyền này.

## Files đã tạo/sửa

### Mới tạo:

- `store/views/admin_views.py` (333 dòng)

### Đã sửa:

- `store/views/__init__.py` - Thêm import admin_views
- `store/urls.py` - Thêm 14 URL patterns mới

## Luồng hoạt động tự động

### 1. Quy trình xử lý đơn hàng

```
Order created (pending)
    ↓
Payment confirmed → Order (processing)
    ↓
Shipping assigned → Shipping (assigned)
    ↓
Shipping picked up → Shipping (picked_up)
    ↓
Shipping in transit → Shipping (in_transit)
    ↓
Shipping delivered → Order (completed)
```

### 2. Tracking tự động

Mỗi lần update shipping status sẽ tự động tạo Tracking record mới với:

- Location
- Status
- Timestamp
- Note (optional)

## Templates cần tạo

Để hoàn thiện giao diện, cần tạo các templates sau trong `store/templates/admin/`:

1. `users_list.html`
2. `user_detail.html`
3. `create_staff.html`
4. `orders_list.html`
5. `order_detail.html`
6. `payments_list.html`
7. `shippings_list.html`
8. `shipping_detail.html`

## Tính năng nổi bật

1. **Quản lý người dùng toàn diện**: Xem, tìm kiếm, kích hoạt/vô hiệu hóa, tạo staff
2. **Quản lý đơn hàng tập trung**: Xem tất cả orders, cập nhật trạng thái, thống kê doanh thu
3. **Quản lý thanh toán**: Xác nhận thanh toán, tự động cập nhật order status
4. **Quản lý vận chuyển**: Gán shipper, tracking chi tiết, tự động hoàn tất đơn hàng khi delivered
5. **Phân quyền chặt chẽ**: Chỉ admin/manager mới truy cập được
6. **Thống kê realtime**: Doanh thu, tổng số tiền thanh toán

## Lưu ý

- Tất cả chức năng đã sử dụng DAOs theo chuẩn kiến trúc
- Logic tự động giữa Payment, Shipping và Order đã được kết nối
- Có thể dễ dàng mở rộng thêm chức năng quản lý khác
