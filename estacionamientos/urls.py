# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from estacionamientos import views
from estacionamientos.views import *
from billetera.views import billetera_pagar
from reservas.views import *


# Este error es raro, en django funciona
urlpatterns = patterns('',
    
    # Estacionamiento                   
    
    url(r'^$', views.estacionamientos_all, name = 'estacionamientos_all'),
    url(r'^(?P<_id>\d+)/$', views.estacionamiento_detail, name = 'estacionamiento_detail'),
    url(r'^(?P<_id>\d+)/reserva$', views.estacionamiento_reserva, name = 'estacionamiento_reserva'),
    url(r'^(?P<_id>\d+)/pago$', views.estacionamiento_pago, name = 'estacionamiento_pago'),
    url(r'^(?P<_id>\d+)/billeterapagar$', billetera_pagar, name = 'billetera_pagar'),
    url(r'^(?P<_id>\d+)/modopago$', views.estacionamiento_modo_pago, name = 'modo_pago'),
    url(r'^ingreso$', views.estacionamiento_ingreso, name = 'estacionamiento_ingreso'),
    
    # Consultar Reservas
    
    url(r'^consulta_reserva$', Consulta_reserva, name = 'estacionamiento_consulta_reserva'),
    url(r'^consulta_reserva/(?P<_id>\d+)$', reserva_detalle, name = 'estacionamiento_consulta_reserva'),
    
    # Cancelar Reserva
    
    url(r'^cancelar_reserva$', estacionamiento_cancelar_reserva, name = 'estacionamiento_cancelar_reserva'),
    url(r'^cancelar_reserva/confirmar$', confirmar_cancelar_reserva, name = 'confirmar_cancelar_reserva'),
    
    # Mover Reserva
    
    url(r'^mover_reserva$', Mover_reserva_buscar_original, name = 'Mover_reserva_buscar_original'),
    url(r'^mover_reserva/buscar_nueva$', Mover_Reserva_buscar_nueva, name = 'Mover_reserva_buscar_nuevo'),
    url(r'^mover_reserva/Confirmar$', Mover_Reserva_Confirmar, name = 'Mover_Reserva_Confirmar'),

    # SMS
    
    url(r'^sms$', views.receive_sms, name='receive_sms'),
    
    # Tasas de Reservacion
    
    url(r'^(?P<_id>\d+)/tasaDiscapacitados$', views.tasa_de_reservacionDiscapacitados, name = 'tasa_de_reservacionDiscapacitados'),
    url(r'^(?P<_id>\d+)/tasaPesados$', views.tasa_de_reservacionPesados, name = 'tasa_de_reservacionPesados'),
    url(r'^(?P<_id>\d+)/tasaMotos$', views.tasa_de_reservacionMotos, name = 'tasa_de_reservacionMotos'),
    url(r'^(?P<_id>\d+)/tasaLivianos$', views.tasa_de_reservacionLivianos, name = 'tasa_de_reservacionLivianos'),
    
    
    url(r'^grafica/.*$', views.grafica_tasa_de_reservacion, name = 'grafica_tasa_de_reservacion'),
    
    # Editar estacionamiento
    
    url(r'^(?P<_id>\d+)/editar$', views.estacionamiento_editar, name = 'estacionamiento_editar'),
    
    # Dias feriados
    
    url(r'^(?P<_id>\d+)/diasFeriados$', views.Estacionamiento_Dias_Feriados, name = 'Estacionamiento_Dias_Feriados'),
    url(r'^(?P<_id>\d+)/agregar_dia_extra$',views.Estacionamiento_Dia_Feriado_Extra, name = 'Dia_Feriado_Extra'),
    url(r'^(?P<_id>\d+)/catalogo_dias_feriados$', views.Mostrar_Dias_Feriados, name = 'Estacionamiento_Dias_Feriados'),

)
