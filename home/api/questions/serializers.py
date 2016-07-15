from rest_framework import serializers

from home.models import Question


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = [
            'id',
            'author',
            'author_name',
            'ama',
            'question',
            'pub_date'
        ]
