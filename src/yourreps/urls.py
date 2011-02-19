import os.path
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^search/', 'yourreps.views.search'),
    (r'^lookup/', 'yourreps.views.lookup'),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    static_path = os.path.join(settings.PROJECT_DIR, '..', '..', 'static')
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': static_path}))
