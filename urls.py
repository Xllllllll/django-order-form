# -*- coding: utf-8 -*-
from django.conf.urls.defaults import * 

urlpatterns = patterns('order.views',
    url(r'^$', 'order'),
)