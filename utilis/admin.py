import json

from django.contrib import admin
from reversion.admin import VersionAdmin
from reversion.models import Revision, Version

from .models import DummyModel

##reversions#
class VersionAdminModel(admin.StackedInline):
   model = Version
   extra = 0

   fieldsets = (
      (None,
         {
         'fields': (
               'object_id','serialized_data',
         )
         }
      ),
   )
      
   def has_add_permission(self, request, obj=None):
      return False
   
   def has_change_permission(self, request, obj=None):
      return False
   
   def has_delete_permission(self, request, obj=None):
      return False
   
@admin.action(description='Reverted Data')
def revert_data(modeladmin, request, queryset):
   for i in queryset:
      i.revert(delete=False)
                  
@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
   list_display = ("id",'user', 'version_data', 'comment', 'date_created')
   list_display_links = ("id",'user', 'version_data')
   list_filter = ('date_created','version__content_type', 'version__object_id')
   list_per_page = 8
   ordering = ('-date_created',)
   search_fields = ('comment', 'version__serialized_data',)
   
   inlines = (VersionAdminModel, )
   actions = (revert_data,)

   fieldsets = (
      (None,
         {
         'fields': (
               ('user','comment'),
               'date_created',
         )
         }
      ),
   )

   def version_data(self,obj):
      serialized_data = obj.version_set.all().values_list('serialized_data',flat=True)
      final_data = []
      for item in serialized_data:
         try:
               item = json.loads(item)
               data = [{'model': i.get('model'), 'pk': i.get('pk')} for i in item]
               final_data.extend(data)
         except:
               pass
      return final_data 
      
   def has_add_permission(self, request, obj=None):
      return False
      
   def has_delete_permission(self, request, obj=None):
      if request.user.is_superuser:
         return True
      return False

   def has_view_permission(self, request, obj=None):
      if request.user.is_superuser:
         return True
      return False

   def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
      context.update({
         'show_save_and_continue': False,
         'show_save_and_add_another': False,
      })
      return super().render_change_form(request, context, add, change, form_url, obj)
   
   def save_model(self, request, obj, form, change) -> None:
      return obj.revert()
##reversione#
admin.site.register(DummyModel, VersionAdmin)