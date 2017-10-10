from django.contrib.auth.models import User
from django.db import models

class Participants(models.Model):
	id_user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length = 30, db_column='Name', verbose_name=u'Имя')
	second_name = models.CharField(max_length=50, null=True, blank=True, db_column='SecondName', verbose_name=u'Отчество')
	surname = models.CharField(max_length=50, db_column='Surname', verbose_name=u'Фамилия')
	birthday = models.DateField(db_column='Birthday', verbose_name=u'Дата рождения')

	SEX = (
		('M', 'Men'),
		('W', 'Women')
	)
	sex = models.CharField(max_length=1, choices=SEX, default='M', db_column='Sex', verbose_name=u'Пол')
	
	class Meta:
		db_table = 'participants'
		verbose_name = u'Участник'
		verbose_name_plural = u'Участники'
		

