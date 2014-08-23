from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns(
    'webchime.views',
    url(r'^visitor/$', 'visitor_1'),
    url(r'^receiver/$', 'receiver_1'),
)

urlpatterns += staticfiles_urlpatterns()
