from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('users/', include('users.urls')),

    # JWT authentication
    path('token/', TokenObtainPairView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
