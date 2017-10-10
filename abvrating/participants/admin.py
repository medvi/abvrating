from django.contrib import admin
from participants.models import Participants

@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
	list_display = ('name', 'second_name', 'surname', 'birthday', 'sex')
