from django.conf.urls import patterns, include, url
from django.contrib import admin
from DES import views as dviews
from Hill import views as hviews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crypto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', dviews.home, name='home'),
    url(r'^practices/', dviews.practices, name='practices'),

	url(r'^des-process/', dviews.Process.as_view(), name="des-process"),
	url(r'^hill-form/', hviews.hill_form, name="hill-form"),
	url(r'^get_zip/(?P<temp_zip>.{0,12})/$', hviews.get_zip, name='opmodes-get_zip'),
    url(r'^get_img/(?P<temp_img>.{0,15})/$', hviews.get_img, name='opmodes-get_img'),
    url(r'^decrypt/$', hviews.modes_operation_decrypt, name='opmodes-decrypt'),
    url(r'^encrypt/$', hviews.modes_operation_encrypt, name='opmodes-encrypt'),
)
