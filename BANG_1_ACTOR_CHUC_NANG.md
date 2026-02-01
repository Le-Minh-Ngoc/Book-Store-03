# Bảng 1: Actor và Chức năng tương ứng

## Assignment 03: Bookstore Management System

---

| STT | Actor                                         | Chức năng                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| --- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | **Khách hàng (Customer)**                     | - Đăng ký tài khoản<br>- Đăng nhập hệ thống<br>- Cập nhật thông tin cá nhân<br>- Quản lý địa chỉ giao hàng<br>- Tìm kiếm sách theo tiêu đề, tác giả, thể loại<br>- Xem chi tiết sách (mô tả, giá, đánh giá)<br>- Đánh giá và bình luận sách<br>- Thêm sách vào wishlist<br>- Thêm sách vào giỏ hàng<br>- Cập nhật số lượng trong giỏ hàng<br>- Xóa sách khỏi giỏ hàng<br>- Áp dụng mã giảm giá (voucher)<br>- Đặt hàng và thanh toán<br>- Xem lịch sử đơn hàng<br>- Theo dõi trạng thái đơn hàng<br>- Theo dõi vận chuyển bằng mã tracking<br>- Hủy đơn hàng (nếu đang pending)<br>- Nhận gợi ý sách từ hệ thống<br>- Xem lịch sử tìm kiếm |
| 2   | **Quản trị viên (Admin)**                     | - Quản lý người dùng (xem, tìm kiếm, kích hoạt/vô hiệu hóa)<br>- Tạo tài khoản nhân viên<br>- Xem chi tiết thông tin người dùng<br>- Quản lý tất cả đơn hàng<br>- Xem chi tiết đơn hàng (items, payment, shipping)<br>- Cập nhật trạng thái đơn hàng<br>- Xem và quản lý thanh toán<br>- Xác nhận/cập nhật trạng thái thanh toán<br>- Quản lý vận chuyển<br>- Gán shipper cho đơn hàng<br>- Cập nhật trạng thái vận chuyển<br>- Xem thống kê doanh thu<br>- Xem thống kê đơn hàng theo trạng thái                                                                                                                                          |
| 3   | **Quản lý (Manager)**                         | - Truy cập dashboard tổng quan<br>- Quản lý danh mục sách<br>- Thêm sách mới vào hệ thống<br>- Cập nhật thông tin sách<br>- Xóa sách khỏi hệ thống<br>- Kiểm tra tồn kho<br>- Xem báo cáo sách bán chạy<br>- Xem báo cáo sách tồn kho thấp<br>- Quản lý sách hỏng/lỗi<br>- Báo cáo sách hỏng<br>- Xem thống kê sách hỏng                                                                                                                                                                                                                                                                                                                   |
| 4   | **Nhân viên nhập kho (Staff/Warehouse)**      | - Quản lý kho hàng<br>- Tạo phiếu nhập kho mới<br>- Thêm chi tiết sách vào phiếu nhập<br>- Xem danh sách phiếu nhập<br>- Xem chi tiết phiếu nhập kho<br>- Cập nhật số lượng tồn kho<br>- Kiểm tra tồn kho theo kho<br>- Quản lý thông tin nhà cung cấp                                                                                                                                                                                                                                                                                                                                                                                     |
| 5   | **Nhân viên giao hàng (Shipper)**             | - Xem danh sách đơn được gán<br>- Cập nhật trạng thái vận chuyển<br>- Thêm thông tin tracking (vị trí, ghi chú)<br>- Xác nhận đã lấy hàng<br>- Xác nhận đang vận chuyển<br>- Xác nhận giao hàng thành công<br>- Báo cáo giao hàng thất bại                                                                                                                                                                                                                                                                                                                                                                                                 |
| 6   | **Hệ thống thanh toán (Payment System)**      | - Nhận yêu cầu thanh toán từ đơn hàng<br>- Xử lý giao dịch thanh toán<br>- Xác nhận kết quả thanh toán<br>- Gửi thông báo thanh toán thành công/thất bại<br>- Tạo mã giao dịch (transaction ID)<br>- Lưu lịch sử giao dịch<br>- Xử lý hoàn tiền (refund)                                                                                                                                                                                                                                                                                                                                                                                   |
| 7   | **Hệ thống vận chuyển (Shipping System)**     | - Nhận yêu cầu giao hàng từ đơn hàng<br>- Tạo mã tracking number<br>- Tạo thông tin địa chỉ giao hàng<br>- Cập nhật trạng thái vận chuyển<br>- Lưu lịch sử tracking<br>- Gửi thông báo cập nhật cho khách hàng<br>- Xác nhận giao hàng thành công                                                                                                                                                                                                                                                                                                                                                                                          |
| 8   | **Module gợi ý sách (Recommendation Engine)** | - Phân tích lịch sử mua hàng của khách<br>- Phân tích wishlist của khách<br>- Phân tích lịch sử tìm kiếm<br>- Tìm sách có cùng thể loại<br>- Tìm sách có cùng tác giả<br>- Sinh danh sách sách gợi ý cá nhân hóa<br>- Hiển thị sách trending (bán chạy)<br>- Hiển thị sách mới về (new arrivals)<br>- Gợi ý sách tương tự khi xem chi tiết                                                                                                                                                                                                                                                                                                 |

---

## Phân loại Actor

### Actor người dùng (Human Actors)

- Khách hàng
- Quản trị viên
- Quản lý
- Nhân viên nhập kho
- Nhân viên giao hàng

### Actor hệ thống (System Actors)

- Hệ thống thanh toán
- Hệ thống vận chuyển
- Module gợi ý sách

---

## Tổng kết chức năng theo Actor

| Actor               | Số lượng chức năng |
| ------------------- | ------------------ |
| Khách hàng          | 19 chức năng       |
| Quản trị viên       | 13 chức năng       |
| Quản lý             | 11 chức năng       |
| Nhân viên nhập kho  | 8 chức năng        |
| Nhân viên giao hàng | 7 chức năng        |
| Hệ thống thanh toán | 7 chức năng        |
| Hệ thống vận chuyển | 7 chức năng        |
| Module gợi ý        | 9 chức năng        |
| **Tổng cộng**       | **81 chức năng**   |

---

## Ghi chú

- Tất cả chức năng đã được triển khai đầy đủ trong code
- Mỗi chức năng có view/DAO tương ứng
- Phân quyền được kiểm tra chặt chẽ cho từng actor
- Hệ thống đảm bảo tính bảo mật và phân quyền rõ ràng
