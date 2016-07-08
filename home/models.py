from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, reverse_lazy


class AMA(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('ama_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title[:20] + " " + str(self.id)

    def clean(self):
        if self.title == '':
            raise ValidationError('Title field can not be empty')


class Comment(models.Model):
    author = models.ForeignKey(User)
    comment = models.CharField(max_length=400)
    pub_date = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    target = fields.GenericForeignKey('content_type', 'object_id')

    comments = fields.GenericRelation('self')

    def __str__(self):
        return self.author.username + "- " + self.comment[:20]


class Question(models.Model):
    author = models.ForeignKey(User, null=True)
    author_name = models.CharField(max_length=25, default='Anonymous')
    ama = models.ForeignKey(AMA, on_delete=models.CASCADE)
    question = models.CharField(max_length=400)
    pub_date = models.DateTimeField(default=timezone.now)
    comments = fields.GenericRelation(Comment)

    def __str__(self):
        return self.author_name + "- " + self.question[:20]


class Answer(models.Model):
    author = models.ForeignKey(User)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=400)
    pub_date = models.DateTimeField(default=timezone.now)
    comments = fields.GenericRelation(Comment)

    def __str__(self):
        return self.author.username + "- " + self.answer[:20]
