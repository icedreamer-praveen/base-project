import hashlib

from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


def make_hash(*keys):
   str_keys = [str(key) for key in keys]
   return hashlib.md5("".join(str_keys).encode("utf-8")).hexdigest()


class CacheMiddleware(MiddlewareMixin):

   def __call__(self, request):
      path = request.META['PATH_INFO']

      if '/api/v1/' in path and request.method in ['GET', 'HEAD']:   
            
         key = [request.get_full_path(),]
         key = make_hash(key)
         cache_key = f'backend:{key}'
         cached_response = cache.get(cache_key)
         
         if cached_response is not None:
               print('from cache')
               return cached_response
         else:
            response = self.get_response(request)
            if response.status_code != 200:
               return response

            viewset = response.renderer_context['view']
            suffix = viewset.suffix if hasattr(viewset, 'suffix') else 'list'
            if suffix != 'Instance':
               try:
                  queryset = viewset.queryset
                  name = f'backend:{queryset.model.__module__}_{queryset.model.__name__}'

                  cache_list = cache.get(name, set())
                  cache_list.add(cache_key)
                  cache.set(name, cache_list)
                  cache.set(cache_key, response)
               except:
                  pass
            return response
      else:
         return self.get_response(request)
      