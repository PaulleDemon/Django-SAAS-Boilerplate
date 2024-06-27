from django.db import models



class ActiveUsersManager(models.Manager):
    
    """ 
        manager that filters out inactive users
    """
    
    # _queryset_class = PostQuerySet

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_admin=False)
 
