from rest_framework import generics, status
from rest_framework.views import APIView, Response

from posts.models import Post
from posts.serializers import PostsSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer

    def create(self, request):
        data = request.data
        data.update({"author": request.user.pk})

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
            
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
