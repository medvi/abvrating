import os
import sys
import django
import datetime

#sys.path.append("/Users/dmedvedev/Documents/Projects/abvrating/abvrating")
os.environ['DJANGO_SETTINGS_MODULE'] = 'abvrating.settings'
django.setup()

from django.contrib.auth.models import User
from index.models import Participant
from index.models import Organization 
from index.models import Organizator 
from index.models import TournamentSeries
from index.models import Tournament
from index.models import UsersRating

User.objects.exclude(username='dmedvedev').delete()
print("Users deleted!")
Participant.objects.all().delete()
print("Participants deleted!")
Organization.objects.all().delete()
print("Organizations deleted!")
Organizator.objects.all().delete()
print("Organizators deleted!")
TournamentSeries.objects.all().delete()
print("TournamentSeties deleted!")
Tournament.objects.all().delete()
print("Tournaments deleted!")
UsersRating.objects.all().delete()
print("UsersRating deleted!")
