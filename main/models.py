from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone

class RunTime(models.Model): 
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="runtimes", null=True)
	title = models.CharField(max_length=200)
	run_time = models.FloatField()
	date = models.DateField(default = timezone.now)

	def __str__(self):
		return self.title


class nickname(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nickname", null=True)
	title = models.CharField(max_length=30)


	def __str__(self):
		return self.title

		







