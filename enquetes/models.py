from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# models a database table that contains questions
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.question_text

# models a database table that contains choice options
class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	def __str__(self):
		return self.choice_text

# models a database table that relates questions to users who have answered them
class UserQuestion(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	#def __str__(self):
	#	return (str(self.user.username())+" "+self.question.question_text)

# models a database table that relates choices to questions in which they appear
class ChoiceQuestion(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
	#def __str__(self):
	#	return self.question.question_text+" "+self.choice.choice_text