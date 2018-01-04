# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

SEX_CHOICES = (
	('M', 'Men'),
	('W', 'Women')
)

class Participant(models.Model):
	user = models.OneToOneField(
		User, on_delete=models.CASCADE, 
		verbose_name='Пользователь'
	)

	name = models.CharField(
		max_length = 30, db_column='Name', 
		verbose_name='Имя', db_index=True
	)

	second_name = models.CharField(
		max_length=50, null=True, blank=True, 
		db_column='SecondName', 
		verbose_name='Отчество', 
		db_index=True
	)

	surname = models.CharField(
		max_length=50, db_column='Surname', 
		verbose_name='Фамилия', 
		db_index=True
	)

	birthday = models.DateField(
		db_column='Birthday', 
		verbose_name='Дата рождения'
	)

	sex = models.CharField(
		max_length=1, choices=SEX_CHOICES, 
		default='M', db_column='Sex', 
		verbose_name='Пол'
	)

	def __str__(self):
		return "{0} {1} {2}".format(
			self.name, self.second_name, self.surname
		)

	class Meta:
		db_table = 'Participants'
		verbose_name = 'Участник'
		verbose_name_plural = 'Участники'
		

class Organization(models.Model):
	users = models.ManyToManyField(
		User, through='Organizator', 
		verbose_name='Пользователи'
	)

	organization_name = models.CharField(
		max_length=100, db_column='OrganizationName', 
		verbose_name='Название организации'
	)

	def __str__(self):
		return "{0}".format(self.organization_name)

	class Meta:
		db_table = 'Organizations'
		verbose_name = 'Организация'
		verbose_name_plural = 'Организации'


class Organizator(models.Model):
	user = models.ForeignKey(
		User, on_delete=models.CASCADE, 
		verbose_name='Пользователь'
	)
	organization = models.ForeignKey(
		Organization, on_delete=models.CASCADE, 
		related_name='employees', 
		verbose_name='Организация', 
		null=True
	)
	participant = models.ForeignKey(
		Participant, on_delete=models.CASCADE, 
		verbose_name='Участник', 
		null=True
	)

	def __str__(self):
		return "{0}: {1}".format(
			self.user.username, 
			self.organization.organization_name
		)

	class Meta:
		db_table = 'Organizators'
		verbose_name = 'Организатор'
		verbose_name_plural = 'Организаторы'


class TournamentSeries(models.Model):
	title = models.CharField(
		max_length=50, db_column='Title', 
		verbose_name='Название', 
		db_index=True
	)

	description = models.TextField(
		db_column='Description', 
		verbose_name='Описание'
	)

	organization= models.ForeignKey(
		Organization, on_delete=models.CASCADE, 
		verbose_name='Организация'
	)

	participants = models.ManyToManyField(
		Participant, through='UsersRating', 
		verbose_name='Участники'
	)

	ts_start_date = models.DateField(
		blank=True, null=True,  
		db_column='TSStartDate', 
		verbose_name='Дата начала серии'
	)

	ts_end_date = models.DateField(
		blank=True, null=True, 
		db_column='TSEndDate', 
		verbose_name='Дата окончания серии'
	)

	def __str__(self):
		return "{0}".format(self.title)

	class Meta:
		db_table = 'TournamentSeries'
		verbose_name = 'Серия турниров'
		verbose_name_plural = 'Серии турниров'


class Tournament(models.Model):
	tournament_series = models.ForeignKey(
		TournamentSeries, on_delete=models.CASCADE, 
		verbose_name='Серия турнира'
	)

	serial_number = models.IntegerField(
		db_column='SerialNumber', 
		verbose_name='Номер в серии'
	)

	priority = models.IntegerField(
		db_column='Priority', 
		verbose_name='Приоритет'
	)

	tournament_start_date = models.DateField(
		blank=True, null=True, 
		db_column='TournamentStartDate', 
		verbose_name='Дата начала турнира'
	)

	tournament_end_date = models.DateField(
		blank=True, null=True, 
		db_column='TournamentEndDate', 
		verbose_name='Дата окончания турнира'
	)

	class Meta:
		db_table = 'Tournaments'
		verbose_name = 'Турнир'
		verbose_name_plural = 'Турниры'


class UsersRating(models.Model):
	participant = models.ForeignKey(
		Participant, on_delete=models.CASCADE, 
		verbose_name='Участник'
	)

	tournament_series = models.ForeignKey(
		TournamentSeries, on_delete=models.CASCADE, 
		verbose_name='Серия турниров'
	)

	rating = models.PositiveIntegerField(
		db_column='Rating', 
		verbose_name='Рейтинг'
	)

	class Meta:
		db_table = 'UsersRating'
		ordering = ['-rating']
		verbose_name = 'Рейтинг'
		verbose_name_plural = 'Рейтинги'
