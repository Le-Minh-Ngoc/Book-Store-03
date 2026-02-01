from store.models import Notification


class NotificationDAO:
    
    @staticmethod
    def create_notification(user, title, message):
        return Notification.objects.create(
            user=user,
            title=title,
            message=message
        )
    
    @staticmethod
    def get_notification_by_id(notification_id):
        try:
            return Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_notifications(user):
        return user.notifications.all()
    
    @staticmethod
    def get_unread_notifications(user):
        return user.notifications.filter(is_read=False)
    
    @staticmethod
    def mark_as_read(notification_id):
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return notification
    
    @staticmethod
    def mark_all_as_read(user):
        user.notifications.update(is_read=True)
    
    @staticmethod
    def delete_notification(notification_id):
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
    
    @staticmethod
    def delete_old_notifications(user, days=30):
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        user.notifications.filter(created_at__lt=cutoff_date).delete()
    
    @staticmethod
    def get_unread_count(user):
        return user.notifications.filter(is_read=False).count()
