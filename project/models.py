from django.db import models

from authentication.models import User


class Project(models.Model):
    title: str = models.CharField(max_length=10, db_index=True)
    description: str = models.CharField(max_length=128)
    creator: User = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title
