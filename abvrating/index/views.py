from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required

from index.forms import *
from index.models import *


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


@login_required
def my_tournament_series_list(request):
	form = TournamentSeriesForm(
		request.POST or None,
		request.FILES or None,
		user=request.user
	)

	if request.method == 'POST':
		if form.is_valid():
			ts = TournamentSeries.objects.create(
				title=form.cleaned_data['title'],
				description=form.cleaned_data['description'],
				organization=form.cleaned_data['organization'],
				ts_start_date=form.cleaned_data['ts_start_date'],
				ts_end_date=form.cleaned_data['ts_end_date'],
				icon=form.cleaned_data['icon'],
			)

			return HttpResponseRedirect('/my_ts/')

	played_ts = TournamentSeries.objects.filter(
		participants__user__username=request.user.username,
	)

	created_ts = TournamentSeries.objects.filter(
		organization__users__username=request.user.username,
	)

	context = {
		"ts_dict": [{
				"ts": created_ts,
				"type": "created",
				"label": "Серии турниров, которые мы организуем"
			},
			{
				"ts": played_ts,
				"type": "played",
				"label": "Серии турниров, в которых я участвую"
			}],
		"form": form,
	}

	return render(request, 'index/my_tournament_series_list.html', context)


def ts_edit(request, ts_id):
	org = Organization.objects.get(users=request.user)
	if not TournamentSeries.objects.filter(
		organization=org, id=ts_id
	).exists():
		return render(request, 'error403.html')

	updated_ts = get_object_or_404(TournamentSeries, id=ts_id)

	form = TournamentSeriesForm(
		request.POST or None, 
		request.FILES or None,
		instance=updated_ts,
		user=request.user
	)

	if request.method == 'POST':
		if form.is_valid():
			updated_ts.icon = form.cleaned_data['icon']
			updated_ts.save();
			return HttpResponseRedirect('/my_ts/')

	context = {
		"form": form,
		"ts": updated_ts,
	}

	return render(request, 'index/ts_edit.html', context)


def ts_delete(request, ts_id):
	deleted_ts = get_object_or_404(TournamentSeries, id=ts_id)    

	if request.method=='POST':
		deleted_ts.delete()
		return HttpResponseRedirect('/my_ts/')

	context = {
	}

	return render(request, 'index/ts_delete', context)


def tournament_series_detail(request, tournament_series_id):
	tournaments_list = \
		Tournament.objects.filter(tournament_series_id=tournament_series_id)

	sort_tournaments_list = \
		tournaments_list.extra(order_by=['tournament_start_date'])

	context = {
		'tournaments': sort_tournaments_list,
	}
	return render(request, 'index/tournament_series_detail.html', context)

def tournament_detail(request, tournament_series_id, tournament_id):
	tournament = Tournament.objects.filter(
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


def register_step1(request):
	initial = {
		'username': request.session.get('username', None),
		'email': request.session.get('email', None),
	}

	form = UserCreationForm(request.POST or None, initial=initial)
	if request.method == 'POST':
		
		if form.is_valid():
			request.session['username'] = form.cleaned_data['username']
			request.session['email'] = form.cleaned_data['email']
			request.session['password'] = form.cleaned_data['password1']

			return HttpResponseRedirect('/accounts/register2/')

	context = {
		'form': form,
	}

	return render(request, 'registration/register1.html', context)


def register_step2(request):
	form = ParticipantCreationForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			request.session['name'] = form.cleaned_data['name']
			request.session['second_name'] = form.cleaned_data['second_name']
			request.session['surname'] = form.cleaned_data['surname']
			request.session['birthday'] = str(form.cleaned_data['birthday'])
			request.session['sex'] = form.cleaned_data['sex']

			print(form.cleaned_data['status'])
			if form.cleaned_data['status'] == '2':
				return HttpResponseRedirect('/accounts/register3/')
			else:
				user = User.objects.create_user(					
					username=request.session['username'],
					email=request.session['email'],
					password=request.session['password'],
				)

				participant = Participant.objects.create(
					user=user,
					name=request.session['name'],
					second_name=request.session['second_name'],
					surname=request.session['surname'],
					birthday=request.session['birthday'],
					sex=request.session['sex'],
				)

				return HttpResponseRedirect('/accounts/login/')

	context = {
		'form': form,
	}

	return render(request, 'registration/register2.html', context)


def register_step3(request):
	form = OrganizatorCreationForm(request.POST or None)

	if request.method == 'POST':
		if form.is_valid():
			user = User.objects.create_user(
				username=request.session['username'],
				email=request.session['email'],
				password=request.session['password'],
			)

			participant = Participant.objects.create(
				user=user,
				name=request.session['name'],
				second_name=request.session['second_name'],
				surname=request.session['surname'],
				birthday=request.session['birthday'],
				sex=request.session['sex'],
			)

			organizator = Organizator.objects.create(
				user=user,
				participant=participant,
				organization=form.cleaned_data['organization']
			)

			return HttpResponseRedirect('/accounts/login/')

	context = {
		'form': form,
	}

	return render(request, 'registration/register3.html', context)
