from rest_framework import serializers

from home.models import AMA


class AMACreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AMA
        fields = [
            'title',
            'description'
        ]


class AMASerializer(serializers.ModelSerializer):

    class Meta:
        model = AMA
        fields = [
            'id',
            'author',
            'title',
            'description',
            'pub_date',
        ]

class AMADetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AMA
        fields = [
            'id',
            'author',
            'title',
            'description',
            'pub_date',
        ]
