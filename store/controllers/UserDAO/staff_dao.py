from store.models import Staff, Manager, Admin, Shipper


class StaffDAO:
    
    @staticmethod
    def create_staff(user):
        staff = Staff.objects.create(user=user)
        return staff
    
    @staticmethod
    def get_staff_by_id(staff_id):
        try:
            return Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            return None
    
    @staticmethod
    def get_staff_by_user(user):
        if hasattr(user, 'staff_profile'):
            return user.staff_profile
        return None
    
    @staticmethod
    def get_all_staff():
        return Staff.objects.all()
    
    @staticmethod
    def delete_staff(staff_id):
        staff = Staff.objects.get(id=staff_id)
        staff.delete()
    
    @staticmethod
    def is_manager(staff):
        return hasattr(staff, 'manager_profile')
    
    @staticmethod
    def is_admin(staff):
        return hasattr(staff, 'admin_profile')
    
    @staticmethod
    def is_shipper(staff):
        return hasattr(staff, 'shipper_profile')
    
    @staticmethod
    def create_manager(staff, department, role=None):
        manager = Manager.objects.create(
            staff=staff,
            department=department,
            role=role
        )
        return manager
    
    @staticmethod
    def create_admin(staff, role=None):
        admin = Admin.objects.create(
            staff=staff,
            role=role
        )
        return admin
    
    @staticmethod
    def create_shipper(staff, vehicle_number, phone):
        shipper = Shipper.objects.create(
            staff=staff,
            vehicle_number=vehicle_number,
            phone=phone
        )
        return shipper
    
    @staticmethod
    def get_all_managers():
        return Manager.objects.all()
    
    @staticmethod
    def get_all_admins():
        return Admin.objects.all()
    
    @staticmethod
    def get_all_shippers():
        return Shipper.objects.all()
