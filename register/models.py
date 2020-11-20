from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class dummyModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dummy", null=True)
	title = models.CharField(max_length=30)


	def __str__(self):
		return self.title