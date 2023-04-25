from email.policy import default
from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    head_image = models.ImageField(upload_to='head_images', default="head_images/default.png")
    
    def __str__(self) -> str:
        return f'Data about {self.user}'

    class Meta:
        verbose_name_plural = 'User Data'
        ordering = ["user"]

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    faculty = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} {self.surname} studying {self.faculty}'

