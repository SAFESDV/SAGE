# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from estacionamientos import views
from billetera.views import billetera_pagar
from reservas.views import *


# Este error es raro, en django funciona
urlpatterns = patterns('',
    url(r'^$', views.estacionamientos_all, name = 'estacionamientos_all'),
    url(r'^(?P<_id>\d+)/$', views.estacionamiento_detail, name = 'estacionamiento_detail'),
    url(r'^(?P<_id>\d+)/reserva$', views.estacionamiento_reserva, name = 'estacionamiento_reserva'),
    url(r'^(?P<_id>\d+)/pago$', views.estacionamiento_pago, name = 'estacionamiento_pago'),
    url(r'^(?P<_id>\d+)/billeterapagar$', billetera_pagar, name = 'billetera_pagar'),
    url(r'^(?P<_id>\d+)/modopago$', views.estacionamiento_modo_pago, name = 'modo_pago'),
    url(r'^ingreso$', views.estacionamiento_ingreso, name = 'estacionamiento_ingreso'),
    url(r'^consulta_reserva$', views.estacionamiento_consulta_reserva, name = 'estacionamiento_consulta_reserva'),
    url(r'^cancelar_reserva$', estacionamiento_cancelar_reserva, name = 'estacionamiento_cancelar_reserva'),
    url(r'^cancelar_reserva/confirmar$', confirmar_cancelar_reserva, name = 'confirmar_cancelar_reserva'),
    url(r'^sms$', views.receive_sms, name='receive_sms'),
    url(r'^(?P<_id>\d+)/tasa$', views.tasa_de_reservacion, name = 'tasa_de_reservacion'),
    url(r'^grafica/.*$', views.grafica_tasa_de_reservacion, name = 'grafica_tasa_de_reservacion'),
    url(r'^(?P<_id>\d+)/editar$', views.estacionamiento_editar, name = 'estacionamiento_editar'),
    url(r'^(?P<_id>\d+)/diasFeriados$', views.Estacionamiento_Dias_Feriados, name = 'Estacionamiento_Dias_Feriados'),
    url(r'^(?P<_id>\d+)/agregar_dia_extra$',views.Estacionamiento_Dia_Feriado_Extra, name = 'Dia_Feriado_Extra'),
)
