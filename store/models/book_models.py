from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .user_models import Customer


class Category(models.Model):
    type = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.type


class Publisher(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    
    class Meta:
        db_table = 'publisher'
    
    def __str__(self):
        return self.name


class Author(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    country = models.CharField(max_length=100)
    address = models.TextField()
    biography = models.TextField(blank=True)
    
    class Meta:
        db_table = 'author'
    
    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=0)
    sold_quantity = models.IntegerField(default=0)
    ISBN = models.CharField(max_length=20, unique=True)
    published_year = models.IntegerField()
    page_count = models.IntegerField()
    language = models.CharField(max_length=50)
    image_url = models.URLField(blank=True, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    authors = models.ManyToManyField(Author, through='BookAuthor', related_name='books')
    categories = models.ManyToManyField(Category, through='BookCategory', related_name='books')
    
    class Meta:
        db_table = 'book'
    
    def __str__(self):
        return self.title


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'book_author'
        unique_together = ('book', 'author')


class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'book_category'
        unique_together = ('book', 'category')


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'book_image'


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'review'
        ordering = ['-created_at']


class Comment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'comment'
        ordering = ['-created_at']


class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlists')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wishlist'
        unique_together = ('customer', 'book')


class DamagedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='damaged_records')
    quantity = models.IntegerField()
    reason = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='reported')
    
    class Meta:
        db_table = 'damaged_book'
        ordering = ['-reported_at']
