from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^ts/$', views.tournament_series_list, name='ts_list'),
	url(r'^ts/(?P<tournament_series_id>[0-9]+)$', views.tournament_series_detail, name='ts_detail'),
	url(r'^ts/(?P<tournament_series_id>[0-9]+)/(?P<tournament_id>[0-9]+)$', views.tournament_detail, name='t_detail'),
	url(r'^rating/(?P<ts_rating_id>[0-9]+)$', views.ts_rating_detail, name='ts_rating_detail')
]
