import os.path
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^search/', 'yourreps.views.search'),
    (r'^lookup/', 'yourreps.views.lookup'),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
