import os
import django
import random
from decimal import Decimal
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore03.settings')
django.setup()

from store.models import (
    User, Customer, Staff, Manager, Category, Publisher, Author,
    Book, BookAuthor, BookCategory, Supplier, Warehouse
)

def create_users():
    print("Tạo users...")
    
    # Tạo hoặc lấy admin user
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@bookstore.com',
            'fullname': 'Quản trị viên',
            'tel': '0123456789',
            'is_staff': True,
            'is_superuser': True,
            'is_staff_member': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print("Đã tạo admin user")
    else:
        print("Admin user đã tồn tại")
    
    # Tạo Manager accounts
    managers_data = [
        {'username': 'manager1', 'email': 'manager1@bookstore.com', 'fullname': 'Nguyễn Quản Lý', 'tel': '0911111111'},
        {'username': 'manager2', 'email': 'manager2@bookstore.com', 'fullname': 'Trần Văn Quản', 'tel': '0922222222'},
    ]
    
    for mgr_data in managers_data:
        user, created = User.objects.get_or_create(
            username=mgr_data['username'],
            defaults={
                'email': mgr_data['email'],
                'fullname': mgr_data['fullname'],
                'tel': mgr_data['tel'],
                'is_staff': True,
                'is_staff_member': True
            }
        )
        if created:
            user.set_password('manager123')
            user.save()
            
            # Tạo Staff profile
            from store.models import Staff, Manager, Role
            staff, _ = Staff.objects.get_or_create(user=user)
            
            # Tạo Manager profile
            manager_role, _ = Role.objects.get_or_create(
                name='Manager',
                defaults={
                    'description': 'Quản lý sách và tồn kho',
                    'permissions': {
                        'can_manage_books': True,
                        'can_manage_inventory': True,
                        'can_view_reports': True
                    }
                }
            )
            Manager.objects.get_or_create(
                staff=staff,
                defaults={
                    'department': 'Quản lý sách',
                    'role': manager_role
                }
            )
            print(f"Đã tạo manager: {mgr_data['username']}")
    
    # Tạo customer accounts
    users_data = [
        {'username': 'nguyenvana', 'email': 'nguyenvana@gmail.com', 'fullname': 'Nguyễn Văn A', 'tel': '0901234567'},
        {'username': 'tranthib', 'email': 'tranthib@gmail.com', 'fullname': 'Trần Thị B', 'tel': '0902234567'},
        {'username': 'levanc', 'email': 'levanc@gmail.com', 'fullname': 'Lê Văn C', 'tel': '0903234567'},
        {'username': 'phamthid', 'email': 'phamthid@gmail.com', 'fullname': 'Phạm Thị D', 'tel': '0904234567'},
        {'username': 'hoangvane', 'email': 'hoangvane@gmail.com', 'fullname': 'Hoàng Văn E', 'tel': '0905234567'},
    ]
    
    customers = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'fullname': user_data['fullname'],
                'tel': user_data['tel']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
        
        from store.models import Customer
        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={'tel': user_data['tel']}
        )
        customers.append(customer)
    
    print(f"Đã kiểm tra/tạo {len(users_data) + len(managers_data) + 1} users, {len(managers_data)} managers, và {len(customers)} customers")
    return customers


def create_categories():
    print("Tạo categories...")
    categories_data = [
        'Văn học',
        'Tiểu thuyết',
        'Khoa học',
        'Lịch sử',
        'Triết học',
        'Kinh tế',
        'Công nghệ',
        'Kỹ năng sống',
        'Thiếu nhi',
        'Truyện tranh',
        'Tâm lý học',
        'Marketing',
    ]
    
    categories = []
    for cat_name in categories_data:
        category, created = Category.objects.get_or_create(type=cat_name)
        categories.append(category)
    
    print(f"Đã tạo {len(categories)} categories")
    return categories


def create_publishers():
    print("Tạo publishers...")
    publishers_data = [
        {'id': 'PUB001', 'name': 'NXB Trẻ', 'address': 'Hà Nội'},
        {'id': 'PUB002', 'name': 'NXB Kim Đồng', 'address': 'TP.HCM'},
        {'id': 'PUB003', 'name': 'NXB Văn học', 'address': 'Hà Nội'},
        {'id': 'PUB004', 'name': 'NXB Lao động', 'address': 'TP.HCM'},
        {'id': 'PUB005', 'name': 'NXB Tổng hợp', 'address': 'Đà Nẵng'},
        {'id': 'PUB006', 'name': 'NXB Thế giới', 'address': 'Hà Nội'},
        {'id': 'PUB007', 'name': 'NXB Phụ nữ', 'address': 'TP.HCM'},
    ]
    
    publishers = []
    for pub_data in publishers_data:
        publisher, created = Publisher.objects.get_or_create(
            id=pub_data['id'],
            defaults={'name': pub_data['name'], 'address': pub_data['address']}
        )
        publishers.append(publisher)
    
    print(f"Đã tạo {len(publishers)} publishers")
    return publishers


def create_authors():
    print("Tạo authors...")
    authors_data = [
        {'id': 'AUT001', 'name': 'Nguyễn Nhật Ánh', 'country': 'Việt Nam', 'birthdate': '1955-05-07', 'address': 'TP.HCM'},
        {'id': 'AUT002', 'name': 'Tô Hoài', 'country': 'Việt Nam', 'birthdate': '1920-09-27', 'address': 'Hà Nội'},
        {'id': 'AUT003', 'name': 'Nam Cao', 'country': 'Việt Nam', 'birthdate': '1915-10-29', 'address': 'Hà Nam'},
        {'id': 'AUT004', 'name': 'Ngô Tất Tố', 'country': 'Việt Nam', 'birthdate': '1894-04-30', 'address': 'Hà Tĩnh'},
        {'id': 'AUT005', 'name': 'Vũ Trọng Phụng', 'country': 'Việt Nam', 'birthdate': '1912-10-20', 'address': 'Hà Nội'},
        {'id': 'AUT006', 'name': 'Haruki Murakami', 'country': 'Nhật Bản', 'birthdate': '1949-01-12', 'address': 'Tokyo'},
        {'id': 'AUT007', 'name': 'Paulo Coelho', 'country': 'Brazil', 'birthdate': '1947-08-24', 'address': 'Rio de Janeiro'},
        {'id': 'AUT008', 'name': 'Dale Carnegie', 'country': 'Mỹ', 'birthdate': '1888-11-24', 'address': 'New York'},
        {'id': 'AUT009', 'name': 'Tony Buzan', 'country': 'Anh', 'birthdate': '1942-06-02', 'address': 'London'},
        {'id': 'AUT010', 'name': 'Stephen Hawking', 'country': 'Anh', 'birthdate': '1942-01-08', 'address': 'Cambridge'},
    ]
    
    authors = []
    for author_data in authors_data:
        author, created = Author.objects.get_or_create(
            id=author_data['id'],
            defaults={
                'name': author_data['name'],
                'country': author_data['country'],
                'birthdate': author_data['birthdate'],
                'address': author_data['address']
            }
        )
        authors.append(author)
    
    print(f"Đã tạo {len(authors)} authors")
    return authors


def create_books(categories, publishers, authors):
    print("Tạo books...")
    books_data = [
        {'title': 'Tôi thấy hoa vàng trên cỏ xanh', 'ISBN': '978-6041111111', 'price': 95000, 'quantity': 50, 'sold_quantity': 120, 'page_count': 368, 'language': 'Tiếng Việt', 'published_year': 2010, 'description': 'Một câu chuyện tình gia đình lắng đọng', 'image_url': 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400&h=600&fit=crop'},
        {'title': 'Cho tôi xin một vé đi tuổi thơ', 'ISBN': '978-6041111112', 'price': 85000, 'quantity': 45, 'sold_quantity': 95, 'page_count': 324, 'language': 'Tiếng Việt', 'published_year': 2012, 'description': 'Những kỷ niệm tuổi thơ đáng nhớ', 'image_url': 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=400&h=600&fit=crop'},
        {'title': 'Dế Mèn phiêu lưu ký', 'ISBN': '978-6041111113', 'price': 65000, 'quantity': 60, 'sold_quantity': 150, 'page_count': 256, 'language': 'Tiếng Việt', 'published_year': 1941, 'description': 'Câu chuyện phiêu lưu của Dế Mèn', 'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=600&fit=crop'},
        {'title': 'Chí Phèo', 'ISBN': '978-6041111114', 'price': 55000, 'quantity': 40, 'sold_quantity': 80, 'page_count': 128, 'language': 'Tiếng Việt', 'published_year': 1941, 'description': 'Tác phẩm văn học kinh điển', 'image_url': 'https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=400&h=600&fit=crop'},
        {'title': 'Tắt đèn', 'ISBN': '978-6041111115', 'price': 75000, 'quantity': 35, 'sold_quantity': 65, 'page_count': 288, 'language': 'Tiếng Việt', 'published_year': 1939, 'description': 'Cuộc sống nông thôn Việt Nam', 'image_url': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=600&fit=crop'},
        {'title': 'Kafka bên bờ biển', 'ISBN': '978-6041111116', 'price': 125000, 'quantity': 30, 'sold_quantity': 85, 'page_count': 512, 'language': 'Tiếng Việt', 'published_year': 2002, 'description': 'Tiểu thuyết nổi tiếng của Murakami', 'image_url': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=600&fit=crop'},
        {'title': 'Nhà giả kim', 'ISBN': '978-6041111117', 'price': 89000, 'quantity': 55, 'sold_quantity': 200, 'page_count': 224, 'language': 'Tiếng Việt', 'published_year': 1988, 'description': 'Hành trình tìm kiếm kho báu', 'image_url': 'https://images.unsplash.com/photo-1589998059171-988d887df646?w=400&h=600&fit=crop'},
        {'title': 'Đắc nhân tâm', 'ISBN': '978-6041111118', 'price': 99000, 'quantity': 70, 'sold_quantity': 350, 'page_count': 320, 'language': 'Tiếng Việt', 'published_year': 1936, 'description': 'Nghệ thuật giao tiếp và ứng xử', 'image_url': 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&h=600&fit=crop'},
        {'title': 'Tư duy mở', 'ISBN': '978-6041111119', 'price': 79000, 'quantity': 45, 'sold_quantity': 120, 'page_count': 256, 'language': 'Tiếng Việt', 'published_year': 1974, 'description': 'Kỹ thuật tư duy sáng tạo', 'image_url': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=600&fit=crop'},
        {'title': 'Lược sử thời gian', 'ISBN': '978-6041111120', 'price': 149000, 'quantity': 25, 'sold_quantity': 60, 'page_count': 256, 'language': 'Tiếng Việt', 'published_year': 1988, 'description': 'Khám phá vũ trụ và thời gian', 'image_url': 'https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop'},
        {'title': 'Con chó nhỏ mang giỏ hoa hồng', 'ISBN': '978-6041111121', 'price': 92000, 'quantity': 42, 'sold_quantity': 78, 'page_count': 400, 'language': 'Tiếng Việt', 'published_year': 2015, 'description': 'Câu chuyện cảm động về tình thân', 'image_url': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=600&fit=crop'},
        {'title': 'Mắt biếc', 'ISBN': '978-6041111122', 'price': 87000, 'quantity': 38, 'sold_quantity': 145, 'page_count': 272, 'language': 'Tiếng Việt', 'published_year': 2007, 'description': 'Tình yêu thơ ngây tuổi học trò', 'image_url': 'https://images.unsplash.com/photo-1476275466078-4007374efbbe?w=400&h=600&fit=crop'},
        {'title': 'Cánh đồng bất tận', 'ISBN': '978-6041111123', 'price': 105000, 'quantity': 33, 'sold_quantity': 72, 'page_count': 384, 'language': 'Tiếng Việt', 'published_year': 2005, 'description': 'Về cuộc sống và tình yêu', 'image_url': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400&h=600&fit=crop'},
        {'title': '7 thói quen hiệu quả', 'ISBN': '978-6041111124', 'price': 115000, 'quantity': 50, 'sold_quantity': 180, 'page_count': 416, 'language': 'Tiếng Việt', 'published_year': 1989, 'description': 'Phát triển bản thân hiệu quả', 'image_url': 'https://images.unsplash.com/photo-1491841573634-28140fc7ced7?w=400&h=600&fit=crop'},
        {'title': 'Tuổi trẻ đáng giá bao nhiêu', 'ISBN': '978-6041111125', 'price': 69000, 'quantity': 60, 'sold_quantity': 220, 'page_count': 288, 'language': 'Tiếng Việt', 'published_year': 2013, 'description': 'Định hướng cho tuổi trẻ', 'image_url': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&h=600&fit=crop'},
    ]
    
    books = []
    for i, book_data in enumerate(books_data):
        publisher = random.choice(publishers)
        
        book, created = Book.objects.get_or_create(
            ISBN=book_data['ISBN'],
            defaults={
                'id': f'BOOK{i+1:03d}',
                'title': book_data['title'],
                'price': book_data['price'],
                'quantity': book_data['quantity'],
                'sold_quantity': book_data['sold_quantity'],
                'page_count': book_data['page_count'],
                'language': book_data['language'],
                'published_year': book_data['published_year'],
                'description': book_data['description'],
                'image_url': book_data['image_url'],
                'publisher': publisher,
            }
        )
        
        # Update image_url if book already exists
        if not created and book.image_url != book_data['image_url']:
            book.image_url = book_data['image_url']
            book.save()
        
        selected_authors = random.sample(authors, min(random.randint(1, 2), len(authors)))
        for author in selected_authors:
            BookAuthor.objects.get_or_create(book=book, author=author)
        
        selected_categories = random.sample(categories, min(random.randint(1, 3), len(categories)))
        for category in selected_categories:
            BookCategory.objects.get_or_create(book=book, category=category)
        
        books.append(book)
    
    print(f"Đã tạo {len(books)} books")
    return books


def create_suppliers():
    print("Tạo suppliers...")
    suppliers_data = [
        {'name': 'Công ty Sách Việt', 'address': 'Hà Nội', 'contact_number': '0241234567', 'email': 'contact@sachviet.com'},
        {'name': 'Công ty Phát hành Sách Trẻ', 'address': 'TP.HCM', 'contact_number': '0281234567', 'email': 'info@sachtre.com'},
        {'name': 'Nhà cung cấp Sách Toàn quốc', 'address': 'Đà Nẵng', 'contact_number': '0236123456', 'email': 'sales@sachtoanquoc.com'},
    ]
    
    suppliers = []
    for sup_data in suppliers_data:
        supplier, created = Supplier.objects.get_or_create(**sup_data)
        suppliers.append(supplier)
    
    print(f"Đã tạo {len(suppliers)} suppliers")
    return suppliers


def create_warehouses():
    print("Tạo warehouses...")
    warehouses_data = [
        {'name': 'Kho Hà Nội', 'location': 'Hà Nội', 'capacity': 10000},
        {'name': 'Kho TP.HCM', 'location': 'TP.HCM', 'capacity': 15000},
        {'name': 'Kho Đà Nẵng', 'location': 'Đà Nẵng', 'capacity': 8000},
    ]
    
    warehouses = []
    for wh_data in warehouses_data:
        warehouse, created = Warehouse.objects.get_or_create(**wh_data)
        warehouses.append(warehouse)
    
    print(f"Đã tạo {len(warehouses)} warehouses")
    return warehouses


def main():
    print("Bắt đầu tạo dữ liệu mẫu...")
    print("="*50)
    
    customers = create_users()
    categories = create_categories()
    publishers = create_publishers()
    authors = create_authors()
    books = create_books(categories, publishers, authors)
    suppliers = create_suppliers()
    warehouses = create_warehouses()
    
    print("="*50)
    print("Hoàn thành tạo dữ liệu mẫu!")
    print(f"Tổng kết:")
    print(f"- Users: {User.objects.count()}")
    print(f"- Customers: {Customer.objects.count()}")
    print(f"- Categories: {Category.objects.count()}")
    print(f"- Publishers: {Publisher.objects.count()}")
    print(f"- Authors: {Author.objects.count()}")
    print(f"- Books: {Book.objects.count()}")
    print(f"- Suppliers: {Supplier.objects.count()}")
    print(f"- Warehouses: {Warehouse.objects.count()}")


if __name__ == '__main__':
    main()
