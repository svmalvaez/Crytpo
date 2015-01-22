from django.conf.urls import patterns, include, url
from django.contrib import admin
from DES import views as dviews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crypto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', dviews.home, name='home'),
    url(r'^practices/', dviews.practices, name='practices'),

    url(r'^des-process/', dviews.Process.as_view(), name="des-process")
)
