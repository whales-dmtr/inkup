from django.contrib import admin

from posts import models


admin.site.register(model_or_iterable=models.Post)