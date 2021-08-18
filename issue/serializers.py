from rest_framework import serializers

from authentication.serializers import UserViewSerializer
from .models import Issue, Comment


class IssueSerializer(serializers.ModelSerializer):
    reporter_details = UserViewSerializer(source='reporter', read_only=True)
    assignee_details = UserViewSerializer(source='assignee', read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)
    status_display_value = serializers.SerializerMethodField('get_status_display_value', read_only=True)
    type_display_value = serializers.SerializerMethodField('get_type_display_value', read_only=True)

    created = serializers.SerializerMethodField(method_name='get_created')
    updated = serializers.SerializerMethodField(method_name='get_updated')
    
    class Meta:
        model = Issue
        fields = ('id', 'title', 'project', 'project_title', 'type', 'type_display_value',
                  'status', 'status_display_value', 'reporter_details', 'assignee_details',
                  'created', 'updated', 'assignee',)
        read_only_fields = ('reporter', 'project')
        extra_kwargs = {
            'assignee': {'write_only': True},
            'type': {'write_only': True},
            'status': {'write_only': True},
        }

    def validate_status(self, value):
        if self.instance and value > self.instance.status + 1:
            raise serializers.ValidationError('Invalid new status provided in request.')
        return value

    def create(self, validated_data):
        reporter = self.context.get('reporter', None)
        project = self.context.get('project', None)

        return Issue.objects.create(reporter=reporter, project=project, **validated_data)

    def get_status_display_value(self, instance):
        return instance.get_status_display()

    def get_type_display_value(self, instance):
        return instance.get_type_display()

    def get_created(self, instance: Issue):
        return instance.created_at.isoformat()

    def get_updated(self, instance: Issue):
        return instance.updated_at.isoformat()


class CommentSerializer(serializers.ModelSerializer):
    author_details = UserViewSerializer(source='author', read_only=True)

    created = serializers.SerializerMethodField(method_name='get_created_at')
    updated = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author_details', 'created', 'updated',)

    def create(self, validated_data):
        author = self.context['author']
        issue = self.context['issue']

        return Comment.objects.create(author=author, issue=issue, **validated_data)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
