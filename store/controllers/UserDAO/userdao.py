from store.models import User
from django.contrib.auth.hashers import make_password
from django.db import transaction


class UserDAO:
    
    @staticmethod
    def create_user(username, email, password, fullname='', tel='', is_staff=False):
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            fullname=fullname,
            tel=tel,
            is_staff_member=is_staff
        )
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_by_username(username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_users():
        return User.objects.all()
    
    @staticmethod
    def update_user(user_id, **kwargs):
        user = User.objects.get(id=user_id)
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        user.save()
        return user
    
    @staticmethod
    def delete_user(user_id):
        user = User.objects.get(id=user_id)
        user.delete()
    
    @staticmethod
    def user_exists(username=None, email=None):
        if username and User.objects.filter(username=username).exists():
            return True
        if email and User.objects.filter(email=email).exists():
            return True
        return False
