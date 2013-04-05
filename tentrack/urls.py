from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from tentrack.models import Player, Week, Match

urlpatterns = patterns('tentrack.views',
    url(r'^$', 'home', name='tentrack_home'),
    url(r'^post/$', 'mpost'),
    url(r'^mentors/$', 'mentors'),
    url(r'^pmatrix/$', 'pmatrix'),
)

urlpatterns += patterns(' ',
    # url(r'^player/$', 'pindex'),
    url(r'^player/$',
        ListView.as_view(
            queryset=Player.objects.order_by('-points'),
            context_object_name='player_list',
            template_name='tentrack/pindex.html')),
    # url(r'^player/(?P<player_id>\d+)/$', 'pdetail'),
    url(r'^player/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Player,
            template_name='tentrack/pdetail.html')),
    # url(r'^week/$', 'windex'),
    url(r'^week/$',
        ListView.as_view(
            queryset=Week.objects.order_by('-id'),
            context_object_name='week_list',
            template_name='tentrack/windex.html')),
    # url(r'^week/(?P<week_id>\d+)/$', 'weekly'),
    url(r'^week/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Week,
            template_name='tentrack/weekly.html'),
        name='tentrack_weekly'),
)
