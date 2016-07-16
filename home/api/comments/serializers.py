from rest_framework import serializers

from home.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='comments-api:detail',
    )
    # delete_url = serializers.HyperlinkedIdentityField(
    #     view_name='comments-api:delete',
    # )

    class Meta:
        model = Comment
        fields = [
            'url',
            'author',
            'comment',
            # 'delete_url',
            'pub_date'
        ]
