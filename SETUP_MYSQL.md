# Hướng dẫn cài đặt và chạy dự án với MySQL

## Bước 1: Cài đặt MySQL Server

1. Tải và cài đặt MySQL Server từ: https://dev.mysql.com/downloads/mysql/
2. Trong quá trình cài đặt, thiết lập password cho tài khoản root (hoặc để trống)
3. Khởi động MySQL Server

## Bước 2: Tạo database

Mở MySQL Command Line hoặc MySQL Workbench và chạy:

```sql
CREATE DATABASE bookstore_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Hoặc chạy file SQL:
```bash
mysql -u root -p < create_database.sql
```

## Bước 3: Cấu hình settings.py

Mở file `bookstore03/settings.py` và cập nhật thông tin database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bookstore_db',
        'USER': 'root',           # Thay đổi nếu cần
        'PASSWORD': '',            # Nhập password của bạn
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

## Bước 4: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

Lưu ý: Nếu gặp lỗi khi cài `mysqlclient` trên Windows:
- Tải file wheel từ: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
- Cài đặt: `pip install mysqlclient-x.x.x-cpXX-cpXX-win_amd64.whl`

## Bước 5: Chạy migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Bước 6: Tạo dữ liệu mẫu

```bash
python seed_data.py
```

## Bước 7: Chạy server

```bash
python manage.py runserver
```

Truy cập: http://127.0.0.1:8000/

## Tài khoản đăng nhập

**Admin:**
- Username: admin
- Password: admin123

**Customer:**
- Username: nguyenvana
- Password: password123

## Kiểm tra database

Sử dụng MySQL Workbench hoặc command line:

```sql
USE bookstore_db;
SHOW TABLES;
SELECT * FROM store_book LIMIT 10;
```
