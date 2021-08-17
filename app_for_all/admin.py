from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(IssueType)
admin.site.register(IssueStatus)
admin.site.register(UserRole)
admin.site.register(Label)

