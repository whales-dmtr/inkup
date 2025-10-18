from rest_framework import generics, mixins

from posts.models import Posts
from posts.serializers import PostsSerializer


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    # lookup_field = 'pk'

    def perform_update(self, serializer):
        print("The instance has updated.")
        instance = serializer.save()

    def perform_destroy(self, instance):
        print("The instance has deleted.")
        super().perform_destroy(instance)


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data.get('content'))
        serializer.save()

