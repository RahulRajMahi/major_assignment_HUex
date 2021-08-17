from django.conf.urls import url
from django.urls.conf import path

from .views import IssueList


urlpatterns = [
    path('issue/', IssueList.as_view()),
    path('issue/<int:id>/', IssueList.as_view()),
]