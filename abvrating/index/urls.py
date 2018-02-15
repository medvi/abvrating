from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^ts/$', views.tournament_series_list, name='ts_list'),
	url(r'^my_ts/$', views.my_tournament_series_list, name='my_ts_list'),
	url(r'^ts/(?P<tournament_series_id>[0-9]+)$', views.tournament_series_detail, name='ts_detail'),
	url(r'^ts/edit/(?P<ts_id>[0-9]+)$', views.ts_edit, name='ts_edit'),
	url(r'^ts/delete/(?P<ts_id>[0-9]+)$', views.ts_delete, name='ts_delete'),
	url(r'^ts/(?P<tournament_series_id>[0-9]+)/(?P<tournament_id>[0-9]+)$', views.tournament_detail, name='t_detail'),
	url(r'^rating/(?P<ts_rating_id>[0-9]+)$', views.ts_rating_detail, name='ts_rating_detail'),
	url(r'^accounts/register1/$', views.register_step1, name="register_step1"),
	url(r'^accounts/register2/$', views.register_step2, name="register_step2"),
	url(r'^accounts/register3/$', views.register_step3, name="register_step3"),
]
