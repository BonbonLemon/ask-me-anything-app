from rest_framework import serializers

from home.models import AMA, Question


class AMAListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='amas-api:detail',
    )
    delete_url = serializers.HyperlinkedIdentityField(
        view_name='amas-api:delete',
    )
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = AMA
        fields = [
            'url',
            'author',
            'title',
            'description',
            'question_count',
            'delete_url',
            'pub_date',
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_question_count(self, obj):
        return obj.questions().count()


class AMACreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AMA
        fields = [
            'title',
            'description',
        ]

class AMAQuestionSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='questions-api:detail',
    #     lookup_field='id',
    # )

    class Meta:
        model = Question
        fields = [
            'id',
            'author',
            'author_name',
            'question',
        ]

    def get_author(self, obj):
        if obj.author is not None:
            return obj.author.username
        return None


class AMADetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = AMA
        fields = [
            'id',
            'author',
            'title',
            'description',
            'questions',
            'pub_date',
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_questions(self, obj):
        return AMAQuestionSerializer(obj.questions(), many=True).data
