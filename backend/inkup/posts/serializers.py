from rest_framework import serializers

from posts.models import Post, Like


class PostsSerializer(serializers.ModelSerializer):
    likes_number = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "time_created",
            "author",
            "likes_number"
        ]

    def get_likes_number(self, obj):
        return Like.objects.filter(post_id=obj.pk).count()