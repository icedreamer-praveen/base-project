import json

from django.db.models.fields.files import ImageField
from rest_framework import serializers
from reversion.models import Revision
from .models import DummyModel


##reversions##
class RevisionSerializer(serializers.ModelSerializer):
   data = serializers.SerializerMethodField()
   class Meta:
      model = Revision
      fields = ('id','date_created', 'user', 'comment', 'data')

   def get_data(self, obj):
      version = obj.version_set.all().values_list('serialized_data', flat=True)
      final_data = []
      for item in version:
            try:
               item = json.loads(item)
               final_data.extend(item)
            except:
               pass
      return final_data 
##reversione##

##imageresizers##
class ThumbnailedImageModelSerilizer(serializers.ModelSerializer):
   def to_representation(self, instance):
      ret = super().to_representation(instance)
      for field in instance._meta._get_fields():
         if isinstance(field, ImageField) and ret[field.name]:
               ret[field.name] = ret[field.name].replace('/mediafiles/', '/thumbnails/mediafiles/') 
      return ret
##imageresizere##

class DummyModelSerializer(ThumbnailedImageModelSerilizer):
   class Meta:
      model = DummyModel
      fields = '__all__'