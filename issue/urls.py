from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IssueViewSet, CommentsListCreateAPIView, CommentsRetrieveDestroyUpdateAPIView

router = DefaultRouter()
router.register(r'issue', IssueViewSet)

app_name = 'issue'

urlpatterns = [
    path('', include(router.urls)),
    path('issue/<int:issue_id>/comment/', CommentsListCreateAPIView.as_view()),
    path('issue/<int:issue_id>/comment/<int:comment_id>/', CommentsRetrieveDestroyUpdateAPIView.as_view()),
]
