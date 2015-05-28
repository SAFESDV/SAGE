# -*- coding: utf-8 -*-


from estacionamientos import views
from django.conf.urls import patterns, url

# Este error es raro, en django funciona
urlpatterns = patterns('',
    url(r'^$', views.estacionamientos_all, name = 'estacionamientos_all'),
    url(r'^propietarios$', views.PropietarioAll, name = 'PropietarioAll'),
    url(r'^(?P<_id>\d+)/$', views.estacionamiento_detail, name = 'estacionamiento_detail'),
    url(r'^(?P<_id>\d+)/editar$', views.estacionamiento_editar, name = 'estacionamiento_editar'),
    url(r'^propietarios/(?P<_id>\d+)/$', views.propietario_editar, name = 'propietario_editar'),
    url(r'^(?P<_id>\d+)/reserva$', views.estacionamiento_reserva, name = 'estacionamiento_reserva'),
    url(r'^(?P<_id>\d+)/pago$', views.estacionamiento_pago, name = 'estacionamiento_pago'),
    url(r'^(?P<_id>\d+)/billeterapagar$', views.billetera_pagar, name = 'billetera_pagar'),
    url(r'^crearbilletera$', views.billetera_crear, name = 'billetera_crear'),
    url(r'^verSaldo$', views.Consultar_Saldo, name = 'billetera_consultar'),
    url(r'^(?P<_id>\d+)/modopago$', views.estacionamiento_modo_pago, name = 'modo_pago'),
    url(r'^ingreso$', views.estacionamiento_ingreso, name = 'estacionamiento_ingreso'),
    url(r'^consulta_reserva$', views.estacionamiento_consulta_reserva, name = 'estacionamiento_consulta_reserva'),
    url(r'^sms$', views.receive_sms, name='receive_sms'),
    url(r'^(?P<_id>\d+)/tasa$', views.tasa_de_reservacion, name = 'tasa_de_reservacion'),
    url(r'^grafica/.*$', views.grafica_tasa_de_reservacion, name = 'grafica_tasa_de_reservacion'),
    url(r'^billeterarecargar$', views.billetera_recargar, name = 'billetera_recargar'),
    url(r'^pagarrecarga$',views.recarga_pago, name = 'recarga_pago'),
)