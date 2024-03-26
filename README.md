## To use project init script

```bash
1) Run projectinit.py
2) Enter new project location(absolute path)
3) Enter new project name
4) Select features to keep(Enter comma seperated values eg: 1,2,3)
```

## <<<< Backend with bolier plate codes >>>>

## Features
## Caching:
   ```Description : Caching middleware capable of caching queryset

   in files : backend > custom_middleware.py, settings.py


   to enable :
      1) custom_middleware.py file should be present in base_dir/
      2) Add 'backend.custom_middleware.CacheMiddleware' to middleware list in settings
      3) Viewset should have 'queryset' property
      4) To flush cache when model instances are added/deleted
         - register signals of respective models in utilis > signals.py
         - signals should be imported in apps.py
```

## Reversions
```
   Description : Enables instances versioning and recovery

   in_files : backend > settings.py, urls.py
              utilis  > models.py, serializers.py, views.py

   to_enable :
      1) Install requirements
      2) Add to settings.py  'reversion', 
      3) Add to urls.py(in root url file) 
      4) GetHistroy(ModelViewSet), RevisionSerializer(serializers.ModelSerializer), 
         VersionAdminModel(admin.StackedInline), RevisionAdmin(admin.ModelAdmin) should be present
      5) Admins should inherit 
         from reversion.admin import VersionAdmin
```
## ImageResizer
   ```
Description : Enables image resizing capability

   in_files : backend > urls.py
              utilis > views.py, serializers.py

   to_enable :
      1) Inherit the ThumbnailedImageModelSerializer in the ModelSerializer being used in the view
   
   use : 
      If the request url is as provided by serializer then the response will be original image stored within the model
      If the request url consists of query params 'height' and 'width' the response will be resized image
```

## DOCKER 
```
1. Install [docker](https://get.docker.com/) and [docker-compose](https://docs.docker.com/compose/install/)
2. Run the server docker-compose up -d
```