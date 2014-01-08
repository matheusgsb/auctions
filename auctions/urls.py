from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auctions.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^error404/$', 'core.views.error404', name='error404'),
    url(r'^error500/$', 'core.views.error500', name='error500'),

    url(r'^$', 'core.views.home', name='home'),
    url(r'^index/$', 'core.views.home', name='home'),
    url(r'^home/$', 'core.views.home', name='home'),
    url(r'^register/$', 'core.views.register', name='register'),
    url(r'^search/$', 'core.views.search', name='search'),
    url(r'^create_auction/$', 'core.views.create_auction', name='create_auction'),
    url(r'^login/$', 'core.views.login', name='login'),
    url(r'^logout/$', 'core.views.logout', name='logout'),
    url(r'^profile/$', 'core.views.profile', name='profile'),
    url(r'^edit_profile/$', 'core.views.edit_profile', name='edit_profile'),
    url(r'^forgot_password/$', 'core.views.forgot_password', name='forgot_password'),
    url(r'^auction/(?P<aid>\d+)/$', 'core.views.auction', name='auction'),
    url(r'^category/(?P<cat>\w+)/$', 'core.views.category', name='category'),
    url(r'^about/$', 'core.views.about', name='about'),
    url(r'^contact/$', 'core.views.contact', name='contact'),

    url(r'^update_auctions/$', 'core.views.update_auctions', name='update_auctions'),

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)