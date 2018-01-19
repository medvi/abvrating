from django import forms 
from django.forms import EmailField
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget
from index.models import *

USER_CREATION_ERRORS = {
	"username": {
		'required': "Обязательно для заполнения",
		'min_length': 3,
	},
	"email": {
		'required': "Обязательно для заполнения",
		'min_length': 5,
	},
	"password1": {
		'required': "Обязательно для заполнения",
		'invalid': "Неверный формат",
	},
	"password1": {
		'required': "Обязательно для заполнения",
	},
	"status": {
		"required": "Обязательно для выбора",
	}
}

TOURNAMENT_SERIES_ERRORS = {
	"icon": {
		"invalid": "ошибка1",
		"missing": "ошибка2",
		"empty": "ошибка3",
		"invalid_image": "ошибка4",
	}
}

STATUS_CHOICES = (
	('1', "participant"),
	('2', "organizator"),
)


class UserCreationForm(forms.Form):
	username = forms.CharField(
		label='Логин', max_length=30, 
		error_messages=USER_CREATION_ERRORS,
		help_text='Должно быть уникальным',
	)
	email = forms.EmailField(
		label='Электронный адрес'
	)
	password1 = forms.CharField(
		label='Пароль',
		widget=forms.PasswordInput(),
		error_messages=USER_CREATION_ERRORS,
		help_text='Должен быть не очевидным',
	)
	password2 = forms.CharField(
		label='Повторить пароль',
		widget=forms.PasswordInput(),
		error_messages=USER_CREATION_ERRORS,
		help_text='Должен совпасть с полем "Пароль"',
	)

	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
		raise forms.ValidationError('Пароли не совпадают.')

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		del self.cleaned_data['username']
		raise forms.ValidationError('Пользователь с таким логином уже существует.')


class ParticipantCreationForm(forms.Form):
	name = forms.CharField(
		label='Имя', max_length=30, 
	)
	second_name = forms.CharField(
		label='Отчество', max_length=50, 
	)
	surname = forms.CharField(
		label='Фамилия', max_length=50, 
	)
	birthday = forms.DateField(
		widget = AdminDateWidget,
		label='Дата рождения (дд.мм.гггг)',
		input_formats=[
			'%Y-%m-%d',
			'%m/%d/%Y',
			'%m/%d/%Y',
			'%d.%m.%Y'
		] 
	)
	sex = forms.ChoiceField(
		choices=SEX_CHOICES, label='Пол', initial='',
		widget=forms.RadioSelect(), required=True,
		error_messages=USER_CREATION_ERRORS
	)
	status = forms.ChoiceField(
		choices=STATUS_CHOICES, label="Статус", initial='',
		widget=forms.RadioSelect(), required=True,
		error_messages=USER_CREATION_ERRORS
	)


class OrganizatorCreationForm(forms.ModelForm):
	organization = forms.ModelChoiceField(
		queryset=Organization.objects.all()
	)

	class Meta:
		model = Organizator
		fields = ('organization', )


class TournamentSeriesForm(forms.ModelForm):
	title = forms.CharField(
		label='Название', max_length=50,
	)
	description = forms.CharField(
		label='Описание', widget=forms.Textarea
	)
	organization = forms.ModelChoiceField(
		label='Организация', queryset=None,
	)
	ts_start_date = forms.DateField(
		widget=AdminDateWidget,
		label='Дата начало серии (дд.мм.гггг)',
		input_formats=[
			'%Y-%m-%d',
			'%m/%d/%Y',
			'%m/%d/%Y',
			'%d.%m.%Y'
		] 
	)
	ts_end_date = forms.DateField(
		widget=AdminDateWidget,
		label='Дата окончания серии (дд.мм.гггг)',
		input_formats=[
			'%Y-%m-%d',
			'%m/%d/%Y',
			'%m/%d/%Y',
			'%d.%m.%Y'
		] 
	)

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(TournamentSeriesForm,  self).__init__(*args, **kwargs)
		self.fields['organization'].queryset = \
			Organization.objects.filter(
				users__username=user.username
			)

	class Meta:	
		model = TournamentSeries
		fields = (
			'title', 'description', 'organization', 
			'ts_start_date', 'ts_end_date',
		)
