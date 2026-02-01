from store.models import Category


class CategoryDAO:
    
    @staticmethod
    def create_category(category_type):
        return Category.objects.create(type=category_type)
    
    @staticmethod
    def get_category_by_id(category_id):
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None
    
    @staticmethod
    def get_category_by_type(category_type):
        try:
            return Category.objects.get(type=category_type)
        except Category.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    @staticmethod
    def update_category(category_id, category_type):
        category = Category.objects.get(id=category_id)
        category.type = category_type
        category.save()
        return category
    
    @staticmethod
    def delete_category(category_id):
        category = Category.objects.get(id=category_id)
        category.delete()
    
    @staticmethod
    def category_exists(category_type):
        return Category.objects.filter(type=category_type).exists()
