from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from utilis.models import DummyModel


#Add all cached models here
@receiver([post_save, post_delete], sender = DummyModel)

def post_save_delete_remove_cache(sender, instance,  *args, **kwargs):
   name = f'euwebsite:{sender.__module__}_{sender.__name__}'
   [cache.delete(i) for i in cache.get(name, [])]
   cache.delete(name)

