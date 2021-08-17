from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Issue


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"

class IssueSerializer(ModelSerializer):
    project_title = CharField(source='projct.title')
    reporter_name = CharField(source='reporter.username')
    assignee_name = CharField(source='assignee.username', default='')
    status_display = SerializerMethodField('get_status_display')
    type_display = SerializerMethodField('get_type_display')
    
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'type',
                     'projct', 'reporter', 'assignee', 'project_title',
                     'reporter_name', 'assignee_name', 'status_display', 'type_display']
        
    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_type_display(self, instance):
        return instance.get_type_display()
