from django.contrib.auth.models import User
from django import forms

from .models import AMA, Question

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class AMAForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = AMA
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    question = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Question
        fields = ['question', 'author_name']
