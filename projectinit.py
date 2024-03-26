#!/bin/python3
import os
import shutil


project_location = input("Enter project location: ")
# project_location = '/home/nabin/Projects/YIL/project-base/'
project_name = input("Enter project name: ")


print('1 : Caching')
print('2 : Reversions')
print('2 : ImageResizer')

features = input('Which features you want to keep(enter csv 1,2,3) : ')

project_path = os.path.join(project_location, project_name)

if os.path.exists(project_path):
   if os.listdir(project_path):
      print("Directory is not empty.")
      while True:
         project_name = input("Enter a different project name: ")
         project_path = os.path.join(project_location, project_name)
         if not os.path.exists(project_path):
               break
         
os.makedirs(project_path)

ignore_dirs = ['.git', 'venv', 'mediafiles', 'staticfiles']

for filename in os.listdir('.'):
   file_path = os.path.join('.', filename)

   if os.path.isfile(file_path):
      shutil.copy(file_path, project_path)

   elif os.path.isdir(file_path):
      if filename == 'backend':
         shutil.copytree(file_path, os.path.join(project_path, project_name))

      elif filename in ignore_dirs:
         continue
      
      else:
         shutil.copytree(file_path, os.path.join(project_path, filename))

print("Project directory created at", project_path)

asgi_path = os.path.join(project_path, project_name, 'asgi.py')
wsgi_path = os.path.join(project_path, project_name, 'wsgi.py')
settings_path = os.path.join(project_path, project_name, 'settings.py')
custom_middleware_path = os.path.join(project_path, project_name, 'custom_middleware.py')
manage_py_path = os.path.join(project_path, 'manage.py')
root_urls_path = os.path.join(project_path, project_name, 'urls.py')
utilis_models_path = os.path.join(project_path, 'utilis', 'models.py')
utilis_serializers_path = os.path.join(project_path, 'utilis', 'serializers.py')
utilis_views_path = os.path.join(project_path, 'utilis', 'views.py')
utilis_admin_path = os.path.join(project_path, 'utilis', 'admin.py')

replace_asg_wsg_manage = [
   "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')"
   ]

replace_pos_settings =  [
   "'backend.custom_middleware.CacheMiddleware',",
   "ROOT_URLCONF = 'backend.urls'",
   "WSGI_APPLICATION = 'backend.wsgi.application'",
   ]

replace_pos_custom =  [
   "cache_key = f'backend:{key}",
   "name = f'backend:{queryset.model.__module__}_{queryset.model.__name__}'"
   ]

def replace_strings_in_file(filepath, replace_strings):
   with open(filepath, 'r') as f:
      file_lines = f.readlines()

   for i, line in enumerate(file_lines):
      for replace_string in replace_strings:
         if replace_string in line:
               new_line = line.replace('backend', project_name)
               file_lines[i] = new_line

   with open(filepath, 'w') as f:
      f.writelines(file_lines)

replace_strings_in_file(settings_path, replace_pos_settings)
replace_strings_in_file(custom_middleware_path, replace_pos_custom)
replace_strings_in_file(asgi_path, replace_asg_wsg_manage)
replace_strings_in_file(wsgi_path, replace_asg_wsg_manage)
replace_strings_in_file(manage_py_path, replace_asg_wsg_manage)


def remove_blocks_from(filepath, start, end):
   with open(filepath, 'r') as file:
      lines = file.readlines()

   with open(filepath, 'w') as file:
      inside_block = False
      for line in lines:
         if start in line:
               inside_block = True
         elif end in line:
               inside_block = False
         elif not inside_block:
               file.write(line)


def remove_lines(filepath, remove_list):
   with open(filepath, 'r') as file:
      lines = file.readlines()

   with open(filepath, 'w') as file:
      for line in lines:
         if not any(remove_str in line for remove_str in remove_list):
               file.write(line)


if len(features) <= 0:
   exit()

choices = features.split(',')

if '1' not in choices:
   print('Removing Caching')
   os.remove(custom_middleware_path)
   remove_blocks_from(settings_path, '##CACHINGs##', '##CACHINGe##')
   print('Removed Caching')


if '2' not in choices:

   settings_remove_list = [
      "'reversion.middleware.RevisionMiddleware',",
      "'reversion',"
   ]
   urls_remove_list = [
      "from utilis.views import GetHistroy",
      "router.register('history', GetHistroy, 'history')"
   ]

   admin_remove_list = [
      'import json',
      'from reversion.admin import VersionAdmin',
      'from reversion.models import Revision, Version',
      'admin.site.register(DummyModel, VersionAdmin)'
   ]

   serializer_remove_list = [
      'from reversion.models import Revision',
   ]

   print('Removing Reversions')
   remove_lines(settings_path, settings_remove_list)
   remove_lines(root_urls_path, urls_remove_list)
   remove_lines(utilis_admin_path, admin_remove_list)
   remove_lines(utilis_serializers_path, serializer_remove_list)
   remove_blocks_from(utilis_models_path, '##reversions#', '##reversione#')
   remove_blocks_from(utilis_serializers_path, '##reversions#', '##reversione#')
   remove_blocks_from(utilis_views_path, '##reversions#', '##reversione#')
   remove_blocks_from(utilis_admin_path, '##reversions#', '##reversione#')
   print('Removed Reversions')


urls_remove_list = [
   "from utilis.views import thumbnails",
	"re_path(r'thumbnails/mediafiles/', thumbnails)"
]

views_remove_list = [
   "import os",
   "from django.http import HttpResponse",
   "from PIL import Image"
]

serializer_remove_list = [
   "from django.db.models.fields.files import ImageField",
]

if '3' not in choices:
   print('Removing imageresizer')
   remove_lines(root_urls_path, urls_remove_list)
   remove_lines(utilis_views_path, views_remove_list)
   remove_lines(utilis_serializers_path, serializer_remove_list)
   remove_blocks_from(utilis_views_path, '##imageresizers##', '##imageresizere##')
   remove_blocks_from(utilis_serializers_path, '##imageresizers##', '##imageresizere##')
   print('Removed imageresizer')
