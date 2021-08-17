from django.db import models
from .models import *
# Create your models here.

class IssueType(models.Model):
    issue_type_name = models.CharField(max_length=255,unique=True,null=False)

class IssueStatus(models.Model):
    issue_status_name = models.CharField(max_length=255,unique=True,null=False)

class UserRole(models.Model):
    user_role_type = models.CharField(max_length=255,unique=True,null=False)

class Label(models.Model):
    label_name = models.CharField(max_length=255,unique=True,null=False)

