from django.urls import path

from posts import views


urlpatterns = [
    path('<int:pk>', views.PostDetailAPIView.as_view()),
    path('<int:pk>/update/', views.PostUpdateAPIView.as_view()),
    path('<int:pk>/delete/', views.PostDeleteAPIView.as_view()),
    path('', views.PostListCreateAPIView.as_view()),
]