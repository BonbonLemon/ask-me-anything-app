from rest_framework import serializers

from home.models import Question


class QuestionListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='questions-api:detail',
    )
    # delete_url = serializers.HyperlinkedIdentityField(
    #     view_name='questions-api:delete',
    # )

    class Meta:
        model = Question
        fields = [
            'url',
            'author',
            'author_name',
            'ama',
            'question',
            # 'delete_url',
            'pub_date'
        ]
