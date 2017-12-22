from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from index.models import TournamentSeries, Tournament, UsersRating

# Create your views here.


def index(request):
	return render(request, 'index/index.html')


def tournament_series_list(request):
	tournament_series_list = TournamentSeries.objects.all()
	paginator = Paginator(tournament_series_list, 24)

	page = request.GET.get('page')
	try:
		tournament_series = paginator.page(page)
	except (PageNotAnInteger, EmptyPage) as e:
		tournament_series = paginator.page(1)	

	context = {
		'tseries': tournament_series,
		'num_pages': paginator.page_range,
	}
	return render(request, 'index/tournament_series_list.html', context)


def tournament_series_detail(request, tournament_series_id):
	tournaments_list = Tournamentxs.objects.filter(tournament_series_id=tournament_series_id)

	context = {
		'tournaments': tournaments_list,
	}
	return render(request, 'index/tournament_series_detail.html', context)

def tournament_detail(request, tournament_series_id, tournament_id):
	tournament = Tournamentxs.objects.filter(
		tournament_series_id=tournament_series_id, 
		id=tournament_id
	).first()

	context = {
		'tournament': tournament,
	}
	return render(request, 'index/tournament_detail.html', context)


def ts_rating_detail(request, ts_rating_id):
	users_rating = UsersRating.objects.filter(tournament_series_id=ts_rating_id)

	context = {
		'users_rating': users_rating,
	}
	return render(request, 'index/ts_rating_detail.html', context)
