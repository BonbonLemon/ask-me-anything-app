from rest_framework import serializers

from home.models import AMA


class AMAListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='amas-api:detail',
    )
    delete_url = serializers.HyperlinkedIdentityField(
        view_name='amas-api:delete',
    )

    class Meta:
        model = AMA
        fields = [
            'url',
            'author',
            'title',
            'description',
            'delete_url',
            'pub_date',
        ]

    def get_author(self, obj):
        return obj.author.username


class AMACreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AMA
        fields = [
            'title',
            'description'
        ]

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
