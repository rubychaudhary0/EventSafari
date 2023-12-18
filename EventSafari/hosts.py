from django_hosts import patterns, host
from django.contrib import admin
from . import admin_urls

host_patterns = patterns('',
    host(r'www', 'main.urls', name='www'),
    host(r'services', 'organizer.urls', name='services'),
    host(r'admin', admin_urls, name='admin'),
)