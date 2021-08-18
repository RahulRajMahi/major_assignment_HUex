from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issue.models import Issue
from .serializers import IssueSerializer
from project.models import Project


class IssueViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    lookup_field = 'id'
    queryset = Issue.objects.select_related('project', 'reporter', 'assignee')
    permission_classes = (IsAuthenticated,)
    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = self.queryset

        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__iexact=title)

        project = self.request.query_params.get('project', None)
        if project:
            queryset = queryset.filter(project_id=project)

        project_title = self.request.query_params.get('project-title', None)
        if project_title:
            queryset = queryset.filter(project__title__iexact=project_title)

        reporter = self.request.query_params.get('reporter', None)
        if reporter:
            queryset = queryset.filter(reporter_id=reporter)

        reporter_username = self.request.query_params.get('reporter-username', None)
        if reporter_username:
            queryset = queryset.filter(reporter__username=reporter_username)

        assignee = self.request.query_params.get('assignee', None)
        if assignee:
            queryset = queryset.filter(assignee_id=assignee)

        assignee_username = self.request.query_params.get('assignee-username', None)
        if assignee_username:
            queryset = queryset.filter(assignee__username=assignee_username)

        return queryset

    def create(self, request, **kwargs):
        serializer_context = {'reporter': request.user}
        serializer_data = request.data.get('issue', {})

        project_title = self.request.query_params.get('project-title', None)
        if project_title:
            try:
                project = Project.objects.get(title__iexact=project_title)
            except ObjectDoesNotExist:
                raise NotFound("Project does not exist")
        else:
            project = self.request.query_params.get('project', None)
            if project:
                try:
                    project = Project.objects.get(id=project)
                except ObjectDoesNotExist:
                    raise NotFound("Project does not exist")
            else:
                raise ValidationError("Project is required.")

        serializer_context['project'] = project

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, id):
        serializer_context = {"request": request}
        try:
            serializer_instance = Issue.objects.get(id=id)
        except ObjectDoesNotExist:
            raise NotFound("An Issue with this id was not found.")

        serializer_data = request.data.get('issue', {})

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)