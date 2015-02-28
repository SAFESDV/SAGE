# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from estacionamientos import views


# Este error es raro, en django funciona
urlpatterns = patterns('',
    url(r'^$', views.estacionamientos_all, name = 'estacionamientos_all'),
    url(r'^(?P<_id>\d+)/$', views.estacionamiento_detail, name = 'estacionamiento_detail'),
    url(r'^(?P<_id>\d+)/reserva$', views.estacionamiento_reserva, name = 'estacionamiento_reserva'),
    url(r'^(?P<_id>\d+)/pago$', views.estacionamiento_pago, name = 'estacionamiento_pago'),
    url(r'^ingreso$', views.estacionamiento_ingreso, name = 'estacionamiento_ingreso'),
)
