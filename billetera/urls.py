# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from billetera import views

# Este error es raro, en django funciona
urlpatterns = patterns('',
    url(r'^$', views.Consultar_Saldo, name = 'billetera_consultar'),
    url(r'^billeterapagar$', views.billetera_pagar, name = 'billetera_pagar'),
    url(r'^crearbilletera$', views.billetera_crear, name = 'billetera_crear'),
    url(r'^verSaldo$', views.Consultar_Saldo, name = 'billetera_consultar'),
    url(r'^billeterarecargar$', views.billetera_recargar, name = 'billetera_recargar'),
    url(r'^pagarrecarga$',views.recarga_pago, name = 'recarga_pago'),

)