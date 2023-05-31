from django.contrib import admin
from django.urls import path, include
from simpleapp.views import add_subscribe, delete_subscribe
from django.views.decorators.cache import cache_page
from rest_framework import routers
from simpleapp import views

router = routers.DefaultRouter()
router.register(r'new', views.NewViewset)
router.register(r'category', views.CategoryViewset)
router.register(r'category', views.CategoryViewset)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
   # подключались к главному приложению с префиксом news/.
   path('news/', include('simpleapp.urls')),
   path('', include('protect.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
   path('i18n/', include('django.conf.urls.i18n')),
   path('', include(router.urls)),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

#<int:pk>