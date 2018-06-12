import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.base import View

from index.forms import *
from index.models import *


def multiply(value, arg):
    return value*arg


def index(request):
	return render(request, 'index/index.html')


def tournament_series_list(request):
	tournament_series_list = TournamentSeries.objects.all()
	sort_ts_list = \
		tournament_series_list.extra(order_by=['id'])
	paginator = Paginator(sort_ts_list, 24)

	page = request.GET.get('page')
	try:
		tournament_series = paginator.page(page)
	except (PageNotAnInteger, EmptyPage) as e:
		tournament_series = paginator.page(1)	

	context = {
		'tseries': tournament_series,
		'num_pages': paginator.page_range,
	}
	return render(request, 'index/ts_list.html', context)


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

	return render(request, 'index/my_ts_list.html', context)


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


def tournament_series_detail(request, ts_id):
	tournaments_list = \
		Tournament.objects.filter(tournament_series_id=ts_id)

	sort_tournaments_list = \
		tournaments_list.extra(order_by=['tournament_start_date'])

	today = datetime.datetime.now()

	context = {
		'tournaments': sort_tournaments_list,
		'mXy': 12*today.year + (today.month-1),
		'ts_id': ts_id,
	}

	return render(request, 'index/ts_detail.html', context)

def tournament_detail(request, tournament_series_id, tournament_id):
	tournament = Tournament.objects.filter(
		tournament_series_id=tournament_series_id, 
		id=tournament_id
	).first()

	context = {
		'tournament': tournament,
	}
	return render(request, 'index/t_detail.html', context)


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


class TournamentCreate(View):
	def get(self, request, ts_id, sdate):
		form = TournamentForm()

		context = {
			'form': form,
			'ts_id': ts_id,
			'sdate': sdate,
		}

		return render(request, 'index/t_create.html', context)

	def post(self, request, ts_id, sdate):
		form = TournamentForm(
			request.POST or None,
			request.FILES or None,
		)

		if form.is_valid():
			print(form)
			tournaments_list = \
				Tournament.objects.filter(tournament_series_id=ts_id)

			sort_tournaments_list = \
				tournaments_list.extra(order_by=['tournament_start_date'])

			max_serial_number = \
				max(tournaments_list.values_list('serial_number', flat=True), default=1)

			t = Tournament.objects.create(
				tournament_series_id=ts_id,
				serial_number=max_serial_number+1,
				priority=form.cleaned_data['priority'],
				tournament_start_date='-'.join([sdate[0:4], sdate[4:6], sdate[6:8]]),
				tournament_end_date=form.cleaned_data['t_end_date'],
				icon=form.cleaned_data['icon'],
			)

			today = datetime.datetime.now()

			context = {
				'ts_id': ts_id,
				'tournaments': sort_tournaments_list,
				'mXy': 12*today.year + (today.month-1),
				'form': form,
			}

			return render(request, 'index/ts_detail.html', context)

		context= {
			'form': form,
			'ts_id': ts_id,
			'sdate': sdate,
		}

		return render(request, 'index/t_create.html', context)


class TournamentDelete(DeleteView):
	model = Tournament
	succes_url = reverse_lazy('ts_detail')
	pk_url_kwarg = 't_id'

	def get_success_url(self):
		ts = self.object.tournament_series 
		return reverse_lazy('ts_detail', kwargs={'ts_id': ts.id})
