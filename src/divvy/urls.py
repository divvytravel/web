
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # admin interface
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # auth
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),

    # static
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index_page'),

    url(r'^trip/', include('apps.trips.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
