from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class AMA(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    description_text = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title[:20] + " " + str(self.id)
    def clean(self):
        if self.title == '':
            raise ValidationError('Title field can not be empty')


class Question(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    author_name = models.CharField(max_length=25, default='Anonymous')
    ama = models.ForeignKey(AMA, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=400)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.author_name + "- " + self.question_text[:20]


class Answer(models.Model):
    author = models.ForeignKey(User)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=400)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.author.username + "- " + self.answer_text[:20]
