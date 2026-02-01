# Checklist Nộp Bài - Assignment 03

## Bookstore Management System

---

## ✅ HOÀN THÀNH

### Chương 1: Xác định và Phân tích yêu cầu

- [x] **Bảng 1: Actor và Chức năng**
  - File: `BANG_1_ACTOR_CHUC_NANG.md`
  - Nội dung: 8 actors, 81 chức năng chi tiết

- [x] **Bảng 2: Các lớp, thuộc tính, methods**
  - File: `BANG_2_CAC_LOP.md`
  - Nội dung: 39 lớp với đầy đủ thuộc tính và phương thức

- [ ] **Biểu đồ lớp Phân tích (>50 lớp)**
  - Cần vẽ bằng tool UML (StarUML, Lucidchart, Draw.io)
  - Copy vào 3 folder: ANALYSIS, DATAMODEL, DESIGN
  - CHÚ Ý: Chỉ có lớp, thuộc tính, quan hệ (chưa có methods)

- [ ] **Biểu đồ Hoạt động (Activity Diagram)**
  - Chọn một use case để vẽ (ví dụ: "Đặt hàng")
  - Hiển thị luồng hoạt động từ đầu đến cuối
  - Viết giải thích ý nghĩa

- [ ] **Biểu đồ Tuần tự (Sequence Diagram)**
  - Chọn một use case (ví dụ: "Thanh toán")
  - Hiển thị tương tác giữa các đối tượng
  - Viết giải thích ý nghĩa

---

### Chương 2: Data Model và Database

- [x] **Database MySQL đã tạo**
  - Database name: `bookstore`
  - 32 tables
  - Charset: utf8mb4

- [x] **Code Django Models với ORM**
  - 4 files models (user, book, order, warehouse)
  - 39 classes
  - Foreign Key, OneToOne, ManyToMany relationships

- [ ] **Screenshot 1: Biểu đồ lớp + ORM code**
  - Chụp màn hình biểu đồ lớp (từ tool UML)
  - Chụp code Django models (models/\*.py)

- [ ] **Screenshot 2: Data model**
  - Chụp ERD từ MySQL Workbench hoặc tool tương tự
  - Hiển thị các bảng và quan hệ

- [ ] **Screenshot 3: Database đã tạo**
  - Chụp MySQL Workbench/phpMyAdmin
  - Hiển thị danh sách tables
  - Hoặc chụp kết quả: `SHOW TABLES;`

---

### Chương 3: Thiết kế

- [x] **Code Django đã sinh hoàn chỉnh**
  - 32 Models
  - 22 DAOs
  - 64 Views
  - 79 URLs

- [x] **Tài liệu DAO, MVC, Monolithic**
  - File: `DAO_MVC_MONOLITHIC.md`
  - Giải thích chi tiết từng pattern
  - Ví dụ code cụ thể

- [ ] **Biểu đồ lớp Design (với methods)**
  - Mở file từ folder DESIGN
  - Bổ sung đầy đủ methods cho mỗi class
  - Dựa vào BANG_2_CAC_LOP.md

- [ ] **Thiết kế các layer**
  - Vẽ diagram các tầng:
    - Presentation Layer (Templates)
    - Controller Layer (Views)
    - Service Layer
    - Data Access Layer (DAOs)
    - Domain Layer (Models)
    - Database Layer

---

### Chương 4: Cài đặt và Triển khai

- [x] **Code đầy đủ chức năng**
  - Tất cả yêu cầu đã được code
  - Test cơ bản đã pass

- [ ] **Mapping Code ↔ Design**
  - Tạo bảng tương ứng:
    - Design Class → Code File
    - Design Method → Code Function
    - Design Relationship → Code Foreign Key

- [ ] **6 Screenshots Giao diện** (Chi tiết trong HUONG_DAN_SCREENSHOTS.md)
  1. [ ] Nhân viên nhập sách
  2. [ ] Khách hàng tìm sách
  3. [ ] Gợi ý sách
  4. [ ] Tạo giỏ hàng
  5. [ ] Thanh toán
  6. [ ] Shipping tracking

---

## 📋 CẦN LÀM TIẾP

### Ưu tiên CAO (Bắt buộc)

1. **Chụp 3 screenshots Database** (30 phút)
   - Biểu đồ lớp + ORM
   - ERD/Data model
   - Database tables

2. **Tạo 6 screenshots Giao diện** (2 giờ)
   - Chuẩn bị dữ liệu mẫu
   - Chạy server và chụp từng màn hình
   - Theo hướng dẫn trong HUONG_DAN_SCREENSHOTS.md

3. **Tạo mapping table Code-Design** (1 giờ)
   - Bảng Excel hoặc Word
   - Map từng class/method

### Ưu tiên TRUNG (Nên có)

4. **Vẽ Activity Diagram** (1 giờ)
   - Use case: Đặt hàng
   - Tool: Draw.io, Lucidchart
   - Viết giải thích

5. **Vẽ Sequence Diagram** (1 giờ)
   - Use case: Thanh toán
   - Tool: Draw.io, Lucidchart
   - Viết giải thích

6. **Vẽ Biểu đồ lớp Phân tích** (2-3 giờ)
   - 39 classes với thuộc tính
   - Relationships
   - Copy vào 3 folders

### Ưu tiên THẤP (Tùy chọn)

7. **Vẽ diagram các layer** (30 phút)
8. **Hoàn thiện Design class diagram** (1 giờ)

---

## 📁 CẤU TRÚC THỦ MỤC NỘP BÀI

```
Book-Store-03/
├── ANALYSIS/
│   └── class_diagram_analysis.png
├── DATAMODEL/
│   ├── class_diagram_analysis.png (copy)
│   └── erd_diagram.png
├── DESIGN/
│   ├── class_diagram_analysis.png (copy)
│   └── class_diagram_design.png (có methods)
│
├── screenshots/
│   ├── database/
│   │   ├── 1_class_diagram_orm.png
│   │   ├── 2_data_model.png
│   │   └── 3_database_tables.png
│   └── giao_dien/
│       ├── 1_nhan_vien_nhap_sach.png
│       ├── 2_tim_sach.png
│       ├── 3_goi_y_sach.png
│       ├── 4_gio_hang.png
│       ├── 5_thanh_toan.png
│       └── 6_tracking.png
│
├── diagrams/
│   ├── activity_diagram.png
│   ├── sequence_diagram.png
│   └── layer_architecture.png
│
├── documents/
│   ├── BANG_1_ACTOR_CHUC_NANG.md (hoặc .pdf)
│   ├── BANG_2_CAC_LOP.md (hoặc .pdf)
│   ├── DAO_MVC_MONOLITHIC.md (hoặc .pdf)
│   ├── CODE_DESIGN_MAPPING.xlsx
│   └── GIAI_THICH_BIEU_DO.md
│
└── code/ (source code Django)
    ├── bookstore03/
    ├── store/
    ├── manage.py
    └── requirements.txt
```

---

## ⚙️ LỆNH CHẠY TRƯỚC KHI NỘP

### 1. Đảm bảo migrations đã chạy

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Tạo dữ liệu mẫu

```bash
python manage.py shell
# Chạy script tạo data mẫu
```

### 3. Test server

```bash
python manage.py runserver
# Mở browser: http://localhost:8000
# Test các chức năng chính
```

### 4. Export requirements

```bash
pip freeze > requirements.txt
```

### 5. Backup database

```bash
# mysqldump hoặc export từ MySQL Workbench
mysqldump -u root -p bookstore > bookstore_backup.sql
```

---

## 📊 ĐÁNH GIÁ HOÀN THÀNH

### Code (100%)

- ✅ Models: 32/32
- ✅ DAOs: 22/22
- ✅ Views: 64/64
- ✅ URLs: 79/79
- ✅ Database: MySQL configured

### Documentation (60%)

- ✅ Bảng 1: Actor
- ✅ Bảng 2: Classes
- ✅ DAO/MVC/Monolithic
- ❌ Activity Diagram
- ❌ Sequence Diagram
- ❌ Class Diagram (Analysis & Design)

### Screenshots (0%)

- ❌ 3 screenshots Database
- ❌ 6 screenshots Giao diện

### Mapping (0%)

- ❌ Code-Design mapping table

---

## 🎯 KẾ HOẠCH HOÀN THIỆN

### Ngày 1: Screenshots (3 giờ)

- Sáng: Setup dữ liệu mẫu, chạy server
- Chiều: Chụp 9 screenshots (3 DB + 6 UI)

### Ngày 2: Diagrams (4 giờ)

- Sáng: Activity + Sequence diagrams
- Chiều: Class diagram (analysis)

### Ngày 3: Hoàn tất (2 giờ)

- Sáng: Mapping table
- Chiều: Review, đóng gói, nộp bài

---

## 📝 LƯU Ý QUAN TRỌNG

1. **Tên file** phải rõ ràng, dễ hiểu
2. **Format** ưu tiên PDF cho documents
3. **Screenshots** phải rõ nét, không bị crop
4. **Code** phải có comments tiếng Việt
5. **README** viết hướng dẫn chạy project

---

**Tổng thời gian ước tính còn lại: 9-10 giờ**
**Deadline: Tuần sau (theo thông báo giáo viên)**

**Chúc bạn hoàn thành tốt assignment!**
