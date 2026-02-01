from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    fullname = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    is_staff_member = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    tel = models.CharField(max_length=20)
    address_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'customer'
    
    def __str__(self):
        return f"Customer: {self.user.username}"


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    
    class Meta:
        db_table = 'staff'
    
    def __str__(self):
        return f"Staff: {self.user.username}"


class Supplier(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    tel = models.CharField(max_length=20)
    email = models.EmailField()
    
    class Meta:
        db_table = 'supplier'
    
    def __str__(self):
        return self.name


class MemberShip(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    point = models.IntegerField(default=0)
    rank = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='memberships')
    
    class Meta:
        db_table = 'membership'
    
    def __str__(self):
        return f"{self.customer} - {self.rank}"


class Address(models.Model):
    num = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    
    class Meta:
        db_table = 'address'
    
    def __str__(self):
        return f"{self.num} {self.street}, {self.city}"


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_histories')
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    device = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'login_history'
        ordering = ['-login_time']


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_histories')
    query = models.CharField(max_length=500)
    search_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'search_history'
        ordering = ['-search_time']


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'role'
    
    def __str__(self):
        return self.name


class Manager(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='manager_profile')
    department = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='managers')
    
    class Meta:
        db_table = 'manager'


class Admin(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='admin_profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='admins')
    
    class Meta:
        db_table = 'admin'


class Shipper(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='shipper_profile')
    vehicle_number = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'shipper'
    
    def __str__(self):
        return f"Shipper: {self.staff.user.username}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notification'
        ordering = ['-created_at']
