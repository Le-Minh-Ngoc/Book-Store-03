from store.models import LoginHistory, SearchHistory


class LoginHistoryDAO:
    
    @staticmethod
    def create_login_record(user, ip_address, device):
        return LoginHistory.objects.create(
            user=user,
            ip_address=ip_address,
            device=device
        )
    
    @staticmethod
    def get_user_login_history(user, limit=20):
        return user.login_histories.all()[:limit]
    
    @staticmethod
    def get_all_login_history():
        return LoginHistory.objects.all()
    
    @staticmethod
    def delete_old_records(days=90):
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        LoginHistory.objects.filter(login_time__lt=cutoff_date).delete()


class SearchHistoryDAO:
    
    @staticmethod
    def create_search_record(user, query):
        return SearchHistory.objects.create(
            user=user,
            query=query
        )
    
    @staticmethod
    def get_user_search_history(user, limit=50):
        return user.search_histories.all()[:limit]
    
    @staticmethod
    def get_all_search_history():
        return SearchHistory.objects.all()
    
    @staticmethod
    def delete_old_records(days=30):
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        SearchHistory.objects.filter(search_time__lt=cutoff_date).delete()
    
    @staticmethod
    def get_popular_searches(limit=10):
        from django.db.models import Count
        
        return SearchHistory.objects.values('query').annotate(
            count=Count('query')
        ).order_by('-count')[:limit]
