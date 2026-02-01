from store.models import Author


class AuthorDAO:
    
    @staticmethod
    def create_author(author_data):
        return Author.objects.create(**author_data)
    
    @staticmethod
    def get_author_by_id(author_id):
        try:
            return Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_authors():
        return Author.objects.all()
    
    @staticmethod
    def search_authors(name):
        return Author.objects.filter(name__icontains=name)
    
    @staticmethod
    def filter_by_country(country):
        return Author.objects.filter(country=country)
    
    @staticmethod
    def update_author(author_id, **kwargs):
        author = Author.objects.get(id=author_id)
        
        for key, value in kwargs.items():
            if hasattr(author, key):
                setattr(author, key, value)
        
        author.save()
        return author
    
    @staticmethod
    def delete_author(author_id):
        author = Author.objects.get(id=author_id)
        author.delete()
    
    @staticmethod
    def get_author_books(author_id):
        author = Author.objects.get(id=author_id)
        return author.books.all()
    
    @staticmethod
    def author_exists(author_id):
        return Author.objects.filter(id=author_id).exists()
