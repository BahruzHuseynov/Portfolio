from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UrlModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls')
    url = models.URLField(max_length=255)

    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'
        ordering = ('-created_at',)

    def __str__(self):
        return self.url
