"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from utilis.views import thumbnails
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from utilis.views import GetHistroy
from utilis.views import DummyModelViewSet

router = DefaultRouter()

router.register('history', GetHistroy, 'history')
router.register('dummy', DummyModelViewSet, 'dummy')

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
	re_path(r'thumbnails/mediafiles/', thumbnails)

]
