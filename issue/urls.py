from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IssueViewSet

router = DefaultRouter()
router.register(r'issue', IssueViewSet)

app_name = 'issue'

urlpatterns = [
    path('', include(router.urls)),
]
