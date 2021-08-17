from django.db import models
from django.db.models.deletion import CASCADE

from authentication.models import User
from project.models import Project


class Issue(models.Model):
    class IssueStatuses(models.IntegerChoices):
        OPEN = 0, 'Open'
        WIP = 1, 'In Progress'
        WIR = 2, 'In Review'
        CODED = 3, 'Code Complete'
        DONE = 4, 'Done'
        
    class IssueType(models.IntegerChoices):
        BUG = 0, 'Bug'
        TASK = 1, 'Task'
        STORY = 2, 'Story'
        EPIC = 3, 'Epic'

    title: str = models.CharField(max_length=10, db_index=True)
    description: str = models.CharField(max_length=128)
    type: IssueType.choices = models.IntegerField(choices=IssueType.choices)
    status: IssueStatuses.choices = models.IntegerField(choices=IssueStatuses.choices, default=IssueStatuses.OPEN)
    projct: Project = models.ForeignKey(Project, on_delete=CASCADE)
    reporter: User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported')
    assignee: User = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='assigned')
    
    def __str__(self) -> str:
        return self.title