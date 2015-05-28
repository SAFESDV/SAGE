# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from propietarios import views


# Este error es raro, en django funciona
urlpatterns = patterns('',
    url(r'^$', views.PropietarioAll, name = 'propietarios_all'),
    url(r'^(?P<_id>\d+)/$', views.propietario_editar, name = 'propietario_editar'),
)