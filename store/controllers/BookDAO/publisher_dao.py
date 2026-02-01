from store.models import Publisher


class PublisherDAO:
    
    @staticmethod
    def create_publisher(publisher_data):
        return Publisher.objects.create(**publisher_data)
    
    @staticmethod
    def get_publisher_by_id(publisher_id):
        try:
            return Publisher.objects.get(id=publisher_id)
        except Publisher.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_publishers():
        return Publisher.objects.all()
    
    @staticmethod
    def search_publishers(name):
        return Publisher.objects.filter(name__icontains=name)
    
    @staticmethod
    def update_publisher(publisher_id, **kwargs):
        publisher = Publisher.objects.get(id=publisher_id)
        
        for key, value in kwargs.items():
            if hasattr(publisher, key):
                setattr(publisher, key, value)
        
        publisher.save()
        return publisher
    
    @staticmethod
    def delete_publisher(publisher_id):
        publisher = Publisher.objects.get(id=publisher_id)
        publisher.delete()
    
    @staticmethod
    def get_publisher_books(publisher_id):
        publisher = Publisher.objects.get(id=publisher_id)
        return publisher.books.all()
    
    @staticmethod
    def publisher_exists(publisher_id):
        return Publisher.objects.filter(id=publisher_id).exists()
