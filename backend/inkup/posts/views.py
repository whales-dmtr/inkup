from rest_framework import generics, status
from rest_framework.views import Response
from rest_framework.exceptions import APIException

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

    def partial_update(self, request, pk):
        post = Post.objects.get(pk=pk)
        data = self.serializer_class(post).data
        
        for k in request.data.keys():
            if k in ["id", "time_created", "author"]:
                raise APIException(f"The \"{k}\" field cannot be edited.")
        data.update(request.data)

        serializer = self.serializer_class(post, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
