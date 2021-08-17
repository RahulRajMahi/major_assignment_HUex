from django.urls.conf import path

from .views import ProjectView



urlpatterns = [
    path('project/', ProjectView.as_view()),
    path('project/<int:id>/', ProjectView.as_view()),
]