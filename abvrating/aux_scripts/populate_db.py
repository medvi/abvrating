# -*- coding: utf-8 -*-

import os
import django
import datetime
import argparse
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abvrating.settings")
django.setup()

from django.contrib.auth.models import User
from index.models import Participant
from index.models import Organization 
from index.models import Organizator 
from index.models import TournamentSeries
from index.models import Tournament
from index.models import UsersRating

global User
global Participant
global Organization
global TournamentSeries
global Tournament
global UsersRating
global users
global participants
global organizers
global tournament_series
global datetime
global args 


def check_not_negative(value):
	ivalue = int(value)
	if ivalue < 0:
		raise argparse.ArgumentTypeError(
				   "{0} is an invalid not negative int value"
				   .format(value)
				)
	return ivalue	


def parse_args():
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'-c', '--count', 
		help='Number of records generated in the database. '\
			 'Default value is 10000.',
		type=check_not_negative,
		default=10000
	)
	parser.add_argument(
		'-p', '--partitions',
		help='Number of partitions for the bulk_create. '\
			 'If 0 then there is no partitions. '\
			 'Default value is 10000.',
		type=check_not_negative,
		default=10000
	)
	parser.add_argument(
		'-tc', '--tournaments',
		help='Number of tournaments in the tournaments series. '\
			 'Default value is 2.',
		type=check_not_negative,
		default=2
	)
	parser.add_argument(
		'-pc', '--participants',
		help='Number of participants in the tournaments. '\
			 'Default value is 100.',
		type=check_not_negative,
		default=100
	)
	
	args = parser.parse_args()

	return args


def populate_users(partitions=10000):
	users = []
	for i in range(args.count):
		u = User(
			username='user{0}'.format(i), 
			password='psw'
		)
		users.append(u)

	User.objects.bulk_create(users, partitions)

	return list(User.objects.values('id'))


def populate_participants(partitions=10000):
	participants = []
	for i in range(args.count):
		p = Participant(
			user_id = users[i]['id'],
			name = 'name{0}'.format(i),
			second_name = 'second_name{0}'.format(i),
			surname = 'surname{0}'.format(i),
			birthday = datetime.datetime.now(),
			sex = 'M'
		)
		participants.append(p)

	Participant.objects.bulk_create(participants, partitions)

	return list(Participant.objects.values('id'))


def populate_organizations(partitions=10000):
	organizations = []
	for i in range(args.count):
		o = Organization(
			organization_name='org_name{0}'.format(i)
		)
		organizations.append(o)

	Organization.objects.bulk_create(organizations, partitions)

	return list(Organization.objects.values('id'))


def populate_organizators(partitions=10000):
	organizators = []

	for i in range(args.count):
		id1 = -1;
		id2 = -1;
		while (id1 == id2):
			id1 = int(random.random() * args.count)
			id2 = int(random.random() * args.count)

		o1 = Organizator(
			user_id=users[id1]['id'],
			organization_id=organizations[i]['id'],
			participant_id=participants[i]['id'],
		)
		o2 = Organizator(
			user_id=users[id2]['id'],
			organization_id=organizations[i]['id'],
		)
		organizators.extend([o1, o2])

	Organizator.objects.bulk_create(organizators, partitions)


def create_description():
	return 'ОТКРЫТА заявка на турнир по волейболу 4ч4 в рамках Игр молодежи Москвы.\n\n' + \
		   'Даты проведения:' + \
		   '18, 19, 25, 26 ноября и 2, 3 декабря 2017г.\n\n' + \
		   'Место проведения:' + \
		   'Академия волейбола (Волгоградский проспект д.32 к.36)\n\n' + \
		   'К участию допускаются:' + \
		   'мужчины и женщины в возрасте от 16 до 35 лет (включительно, на дату начала соревнований);\n' + \
		   'Состав команды: от 4 до 8 человек.' + \
		   'Для участия необходимо правильно заполнить заявку (ФИО, дата рождения, обязательно фото игрока)' + \
		   'и оплатить орг.взнос на сайте мероприятия studentsport.org/imm2017/volleyball4x4\n\n' + \
		   'Подать заявка и оплатить орг.взнос можно до 15 ноября (включительно)'


def populate_tournament_series(partitions=10000):
	now = datetime.datetime.now()

	tournament_series = []
	for i in range(args.count):
		rand_icon = random.randint(1, 3)
		ts = TournamentSeries(
			title='Tournament series title {0}'.format(i),
			description=create_description(),
			organization_id=organizations[i]['id'],
			ts_start_date=now.strftime("%Y-%m-%d"),
			ts_end_date=(now+datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
			icon='uploads/image'+str(random.randint(1, 3))+'.jpg',
		)
		tournament_series.append(ts)

	TournamentSeries.objects.bulk_create(tournament_series, partitions)

	return list(TournamentSeries.objects.values('id'))


def populate_tournaments(partitions=10000):
	now = datetime.datetime.now()

	tournaments = []
	for i in range(args.tournaments*args.count):
		rand_icon = random.randint(1, 3)
		t = Tournament(
			tournament_series_id = tournament_series[i%args.count]['id'],
			serial_number = int(i/args.count)+1,
			priority = i,
			tournament_start_date = now.strftime("%Y-%m-%d"),
			tournament_end_date = (now+datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
			icon='uploads/image'+str(random.randint(1, 3))+'.jpg',
		)
		tournaments.append(t)

	Tournament.objects.bulk_create(tournaments, partitions)


def populate_users_rating(partitions=10000):
	users_rating = []
	for j in range(args.count):
		repeated_id = []
		for i in range(args.participants):
			new_id = random.randint(0, args.count-1)
			while (new_id in repeated_id):
				new_id = random.randint(0, args.count-1)
			repeated_id.append(new_id)

			ur = UsersRating(
				participant_id = participants[new_id]['id'],
				tournament_series_id = tournament_series[j]['id'],
				rating = random.randint(1, 100)
			)
			users_rating.append(ur)

	UsersRating.objects.bulk_create(users_rating, partitions)


args = parse_args()

if args.partitions == 0:
	args.partitions = None

users = populate_users(args.partitions)
print("POPULATE USERS")

participants = populate_participants(args.partitions)
print("POPULATE PARTICIPANTS")

organizations = populate_organizations(args.partitions)
print("POPULATE ORGANIZATIONS")

populate_organizators(args.partitions)
print("POPULATE ORGANIZATORS")

tournament_series = populate_tournament_series(args.partitions)
print("POPULATE TOURNAMENT SERIES")

populate_tournaments(args.partitions)
print("POPULATE TOURNAMENTS")

populate_users_rating(args.partitions)
print("POPULATE USERS RATING")


from django.db import connection
print(len(connection.queries))
#for q in connection.queries:
#	print("\n")
#	print(q['sql'])
