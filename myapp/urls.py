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
    path('SERVICIOS_ELECTRONICOS', views.SERVICIOS_ELECTRONICOS, name='SERVICIOS_ELECTRONICOS'),
    path('CEDIS', views.CEDIS, name='CEDIS'),
    path('BACK_OFFICE', views.BACK_OFFICE, name='BACK_OFFICE'),
    path('OTROS', views.OTROS, name='OTROS'),
    path('SERVICIOS_FINANCIEROS', views.SERVICIOS_FINANCIEROS, name='SERVICIOS_FINANCIEROS'),
    path('TAE', views.TAE, name='TAE'),
    path('SERVICIOS_NO_FINANCIEROS', views.SERVICIOS_NO_FINANCIEROS, name='SERVICIOS_NO_FINANCIEROS'),
    path('CORRESPONSALIAS', views.CORRESPONSALIAS, name='CORRESPONSALIAS'),
    path('ENVIOS', views.ENVIOS, name='ENVIOS'),
    path('REMESAS', views.REMESAS, name='REMESAS'),
    path('PAGO_TDC', views.PAGO_TDC, name='PAGO_TDC'),
    path('AUTENTICACION_DE_CAJEROS', views.AUTENTICACION_DE_CAJEROS, name='AUTENTICACION_DE_CAJEROS'),
    path('SPIN', views.SPIN, name='SPIN'),
    path('OXXO_PREMIA', views.OXXO_PREMIA, name='OXXO_PREMIA'),
    path('RETIROS', views.RETIROS, name='RETIROS'),
    path('RETIROS_SIN_TARJETA', views.RETIROS_SIN_TARJETA, name='RETIROS_SIN_TARJETA'),
    path('TIENDAS', views.TIENDAS, name='TIENDAS'),
    path('BOTONPANICO', views.BOTONPANICO, name='BOTONPANICO'),
]#boton de panico added

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_TEMPLATES, document_root=settings.TEMPLATES_ROOT)