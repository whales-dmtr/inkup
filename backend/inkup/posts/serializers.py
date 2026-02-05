from rest_framework import serializers

from posts.models import Post, Like


class PostsSerializer(serializers.ModelSerializer):
    likes_number = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "time_created",
            "author",
            "likes_number",
            "author_username"
        ]

    def get_likes_number(self, obj):
        print(obj)
        return Like.objects.filter(post_id=obj["pk"]).count()

    def get_author_username(self, obj):
        return obj["author__username"]
