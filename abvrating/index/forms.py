from django import forms 
from django.forms import EmailField
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget
from index.models import *

NAME_ERROR_LIST = {
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


STATUS_CHOICES = (
	('1', "participant"),
	('2', "organizator"),
)


class UserCreationForm(forms.Form):
	username = forms.CharField(
		label='Логин', max_length=30, 
		error_messages=NAME_ERROR_LIST,
		help_text='Должно быть уникальным',
	)
	email = forms.EmailField(
		label='Электронный адрес'
	)
	password1 = forms.CharField(
		label='Пароль',
		widget=forms.PasswordInput(),
		error_messages= NAME_ERROR_LIST,
		help_text='Должен быть не очевидным',
	)
	password2 = forms.CharField(
		label='Повторить пароль',
		widget=forms.PasswordInput(),
		error_messages=NAME_ERROR_LIST,
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
		error_messages=NAME_ERROR_LIST 
	)
	status = forms.ChoiceField(
		choices=STATUS_CHOICES, label="Статус", initial='',
		widget=forms.RadioSelect(), required=True,
		error_messages=NAME_ERROR_LIST
	)


class OrganizatorCreationForm(forms.ModelForm):
	organization = forms.ModelChoiceField(
		queryset=Organization.objects.all()
	)

	class Meta:
		model = Organizator
		fields = ('organization', )
