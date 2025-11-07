from rest_framework import generics, status
from rest_framework.views import Response, APIView
from rest_framework.exceptions import APIException

from posts.models import Post, Like
from posts.serializers import PostsSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer

    def create(self, request):
        data = dict(request.data)
        data.update({"author": request.user.pk})

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
            
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer

    def partial_update(self, request, pk):
        for k in request.data.keys():
            if k in ["id", "time_created", "author"]:
                raise APIException(f"The \"{k}\" field cannot be edited.")

        post = Post.objects.get(pk=pk)
        data = self.serializer_class(post).data
        
        data.update(request.data)

        serializer = self.serializer_class(post, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)


class LikePostAPIView(APIView):
    def post(self, request, post_id):
        user_id = request.user.pk

        if Like.objects.filter(post_id=post_id, user_id=user_id).count():
            raise APIException("This user have already liked this post.")

        new_like = Like(post_id=post_id, user_id=user_id)
        new_like.save()

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        user_id = request.user.pk
        like = Like.objects.filter(post_id=post_id, user_id=user_id)

        if not like:
            raise APIException("This user haven't liked this post.")

        like.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
