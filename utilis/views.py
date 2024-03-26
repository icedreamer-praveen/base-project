import os

import reversion
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from PIL import Image
from rest_framework import permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from reversion.models import Revision, Version

from .models import DummyModel
from .serializers import DummyModelSerializer, RevisionSerializer

##reversions##
class GetHistroy(ModelViewSet):
   queryset = Revision.objects.all()
   serializer_class = RevisionSerializer
   permission_classes = (IsAuthenticated,)
   filter_fields = ('version__object_id','version__content_type','date_created')
   ordering_fields = ('date_created',)
   http_method_names = ['get', 'patch', 'delete']	
   
   def get_queryset(self):
      assert self.queryset is not None, (
         "'%s' should either include a `queryset` attribute, "
         "or override the `get_queryset()` method."
         % self.__class__.__name__
      )

      queryset = self.queryset
      if not self.request.user.is_superuser:
         queryset = queryset.filter(user=self.request.user)
      return queryset
   
   @action(methods=['GET'], detail=False, url_path='deleted-data')
   def list_delete(self, request, *args, **kwargs):
      if not request.query_params.get('content_type'):
         return Response({
               'message':'Please provide content_type to filter data.'
         }, status=400)

      content_type = ContentType.objects.filter(id=request.query_params.get('content_type'))
      if not content_type.exists():
         return Response({
               'message':'Cannot find Content type of this id.'
         }, status=400)
      
      model = content_type.first().model_class()
      if not model:
         return Response({
               'message':'Cannot find model of this id.'
         }, status=400)
      
      if not reversion.is_registered(model):
         return Response({
               'message': f'{model.__name__} model has not been registered with django-reversion'
         }, status=400)
      
      version_queryset = Version.objects.get_deleted(model=model)
      queryset = self.filter_queryset(self.get_queryset())
      queryset = queryset.filter(version__in=version_queryset)

      page = self.paginate_queryset(queryset)
      if page is not None:
         serializer = self.get_serializer(page, many=True)
         return self.get_paginated_response(serializer.data)

      serializer = self.get_serializer(queryset, many=True)
      return Response(serializer.data)
   
   def update(self, request, *args, **kwargs):
      instance = self.get_object()
      instance.revert()
      return Response({'message':'Successfully reverted'})

   @action(methods=['DELETE'], detail=False, url_path='clear-revision')
   def destroy_clear(self, request, *args, **kwargs):
      if not self.request.user.is_superuser:
         return Response({
               'message':'You cannot delete revision.'
         }, status=400)
      
      queryset = self.filter_queryset(self.get_queryset())
      
      if request.query_params.get('ids'):
         ids = request.query_params.get('ids').split(',')        
         queryset = queryset.filter(id__in=ids)
      
      if request.query_params.get('end_data'):
         queryset = queryset.filter(date_created__lt=request.query_params.get('end_data'))

      queryset.delete()
      return Response({'message':'Successfully reverted'})
##reversione##

##imageresizers##
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def thumbnails(request):
   request.path_info = request.path_info.replace('thumbnails/mediafiles/', 'mediafiles/')
   path = request.path_info.replace('/mediafiles/', '')

   height = request.query_params.get("height", 0)
   width = request.query_params.get("width", 0)
   try:
      height = int(height)
      width = int(width)
   except:
      raise ParseError("Height or Width must be integer or number.")
   
   if height or width:
      
      if height > 3000 or width > 3000:
         raise ParseError("Maximum height and width is 3000px allowed.")

      base_dir = str(settings.BASE_DIR)
      media_url = str(settings.MEDIA_URL)
      file_path = base_dir + media_url + path

      if not os.path.exists(file_path):
         raise ParseError("File doesnot exist.")

      with Image.open(file_path) as im:
         im_height = im.height
         im_width =  im.width

         if im_height != height or im_width != width:
            thumbs_dir = base_dir + media_url + 'public/' + 'thumbs/'

            original_file = os.path.basename(file_path).split('.')
            original_filename = original_file[0]
            original_ext = original_file[-1]

            new_thumbs_fullpath = thumbs_dir + original_filename + '_thumb-' + str(height)\
                                    + 'x' + str(width) + '.' + original_ext
            
            if not os.path.exists(new_thumbs_fullpath):
               os.makedirs(os.path.dirname(new_thumbs_fullpath), exist_ok = True)
               
               if height > width:
                  width = im_width/im_height * height
               else:
                  height = im_height/im_width * width

               im = im.convert('RGB')
               exif = im.info.get('exif')
               im=im.resize((int(width*1.5), int(height*1.5)))
               im.save(new_thumbs_fullpath, exif=exif, optimize=True, quality=95, progressive=True) if exif else im.save(
                  new_thumbs_fullpath, optimize=True, quality=95, progressive=True)
               path = new_thumbs_fullpath.replace(base_dir + media_url, '')

            else:
               path = new_thumbs_fullpath.replace(base_dir + media_url, '')

   response = HttpResponse()
   response.status_code = 200
   response['X-Accel-Redirect'] = f'/mediafiles/{path}'
   del response['Content-Type']
   del response['Content-Disposition'] 
   del response['Set-Cookie']
   del response['Cache-Control']
   del response['Expires']      
   return response
##imageresizere##

class DummyModelViewSet(ModelViewSet):
   serializer_class = DummyModelSerializer
   queryset = DummyModel.objects.all()
   permission_classes = [permissions.AllowAny]