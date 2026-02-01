from store.models import Customer, Address, MemberShip
from django.db import transaction


class CustomerDAO:
    
    @staticmethod
    def create_customer(user, tel, address_id=''):
        customer = Customer.objects.create(
            user=user,
            tel=tel,
            address_id=address_id
        )
        return customer
    
    @staticmethod
    def get_customer_by_id(customer_id):
        try:
            return Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return None
    
    @staticmethod
    def get_customer_by_user(user):
        if hasattr(user, 'customer_profile'):
            return user.customer_profile
        return None
    
    @staticmethod
    def get_all_customers():
        return Customer.objects.all()
    
    @staticmethod
    def update_customer(customer_id, **kwargs):
        customer = Customer.objects.get(id=customer_id)
        
        for key, value in kwargs.items():
            if hasattr(customer, key):
                setattr(customer, key, value)
        
        customer.save()
        return customer
    
    @staticmethod
    def delete_customer(customer_id):
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
    
    @staticmethod
    def add_address(customer, num, street, city, country):
        address = Address.objects.create(
            customer=customer,
            num=num,
            street=street,
            city=city,
            country=country
        )
        return address
    
    @staticmethod
    def get_customer_addresses(customer):
        return customer.addresses.all()
    
    @staticmethod
    def delete_address(address_id):
        address = Address.objects.get(id=address_id)
        address.delete()
    
    @staticmethod
    def update_membership(customer, points_to_add):
        membership = customer.memberships.first()
        
        if membership:
            membership.point += points_to_add
            
            if membership.point >= 1000:
                membership.rank = 'gold'
            elif membership.point >= 500:
                membership.rank = 'silver'
            else:
                membership.rank = 'bronze'
            
            membership.save()
        
        return membership
    
    @staticmethod
    def get_customer_memberships(customer):
        return customer.memberships.all()
