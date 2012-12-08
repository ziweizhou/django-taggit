from django.conf.urls.defaults import patterns, url

from taggit import views


urlpatterns = patterns('taggit.views',
    url(r'^list$', 'list_tags', name='taggit-list'),
    url(r'^static/(?P<path>.*)$', views.media, name='taggit-static'),
    url(r'^ajax$', views.ajax, name='taggit-ajax'),
)
