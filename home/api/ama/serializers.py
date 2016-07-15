from rest_framework import serializers

from home.models import AMA


class AMACreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AMA
        fields = [
            'title',
            'description'
        ]


class AMASerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = AMA
        fields = [
            'id',
            'author',
            'title',
            'description',
            'pub_date',
        ]

    def get_author(self, obj):
        return obj.author.username

class AMADetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = AMA
        fields = [
            'id',
            'author',
            'title',
            'description',
            'pub_date',
        ]

    def get_author(self, obj):
        return obj.author.username
