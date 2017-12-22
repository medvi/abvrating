# -*- coding: utf-8 -*-

from django.contrib import admin
from index.models import Participant
from index.models import Organization 
from index.models import Organizator 
from index.models import TournamentSeries
from index.models import Tournament
from index.models import UsersRating

@admin.register(Participant)
class ParticipantsAdmin(admin.ModelAdmin):
	list_display = ('name', 'second_name', 'surname', 'birthday', 'sex')


@admin.register(Organization)
class OrganizationsAdmin(admin.ModelAdmin):
	list_display = ('organization_name', )


@admin.register(Organizator)
class OrganizatorsAdmin(admin.ModelAdmin):
	list_display = ('user', 'organization')


@admin.register(TournamentSeries)
class TournamentSeriesAdmin(admin.ModelAdmin):
	list_display = ('title', 'description') 


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
	list_display = ('tournament_series', 'serial_number', 'priority')


@admin.register(UsersRating)
class UsersRatingAdmin(admin.ModelAdmin):
	list_display = ('participant', 'tournament_series', 'rating')
