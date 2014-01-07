from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auctions.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'core.views.home', name='home'),
    url(r'^index/$', 'core.views.home', name='home'),
    url(r'^home/$', 'core.views.home', name='home'),
    url(r'^register/$', 'core.views.register', name='register'),
    url(r'^create_auction/$', 'core.views.create_auction', name='create_auction'),
    url(r'^login/$', 'core.views.login', name='login'),
    url(r'^logout/$', 'core.views.logout', name='logout'),
    url(r'^profile/$', 'core.views.profile', name='profile'),
    url(r'^edit_profile/$', 'core.views.edit_profile', name='edit_profile'),
    url(r'^forgot_password/$', 'core.views.forgot_password', name='forgot_password'),
    url(r'^auction/(?P<aid>\d+)/$', 'core.views.auction', name='auction'),
    url(r'^category/(?P<cat>\w+)/$', 'core.views.category', name='category'),
    url(r'^about/$', 'core.views.about', name='about'),

)
