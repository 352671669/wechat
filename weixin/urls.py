# -*- coding: utf-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns(
    'weixin.views',
    (r'^$', 'index'),
)
