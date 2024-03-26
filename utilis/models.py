from django.db import models
import reversion

##reversions#
@reversion.register(follow=(), for_concrete_model=True, ignore_duplicates=False, use_natural_foreign_keys=False)
class DummyModel(models.Model):
   field = models.CharField(max_length = 255)
   image_field = models.ImageField(upload_to = 'images/')
##reversione#