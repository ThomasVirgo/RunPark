from django import forms
from django.forms import ModelForm

from .models import *


class TimeForm(forms.ModelForm):

    class Meta:
        model = RunTime
        fields = '__all__'


class nicknameForm(forms.ModelForm):

	class Meta:
		model = nickname
		fields = ['title', 'user']

