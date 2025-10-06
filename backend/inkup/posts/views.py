from rest_framework import generics

from posts.models import Posts
from posts.serializers import PostsSerializer


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    # lookup_field = 'pk'


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data.get('content'))
        serializer.save()


class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    def perform_update(self, serializer):
        print("The instance has updated.")
        instance = serializer.save()


class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    def perform_destroy(self, instance):
        print("The instance has deleted.")
        super().perform_destroy(instance)
