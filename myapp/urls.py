from django.contrib import admin
from django.urls import path
#from myapp.views import hello
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    #path('', views.users)
    path('', views.BASE, name='BASE'),
    path('APLICACIONES', views.APLICACIONES, name='APLICACIONES'),
    path('INTERNET', views.INTERNET, name='INTERNET'),
    path('SEGURIDAD', views.SEGURIDAD, name='SEGURIDAD'),
    path('RED', views.RED, name='RED'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_TEMPLATES, document_root=settings.TEMPLATES_ROOT)