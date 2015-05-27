# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from index import views

# Este error es raro, en django funciona
urlpatterns = patterns('',
    url(r'^$', views.index_page, name = 'index_page'),
)
