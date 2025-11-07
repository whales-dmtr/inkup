from django.urls import path

from posts import views


urlpatterns = [
    path('', views.PostListCreateAPIView.as_view()),
    path('<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:post_id>/like/', views.LikePostAPIView.as_view(), 
         name="like_post"),
]
