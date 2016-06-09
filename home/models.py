from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AMA(models.Model):
    author = models.ForeignKey(User)
    description_text = models.CharField(max_length=400)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.author.username + " " + str(self.id)


class Question(models.Model):
    author = models.ForeignKey(User)
    ama = models.ForeignKey(AMA, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.author.username + "- " + self.question_text[:20]


class Answer(models.Model):
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.author.username + "- " + self.answer_text[:20]
