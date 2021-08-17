from django.http import response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from apps.issue.models import Issue
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import IssueSerializer, IssueListSerializer


class IssueList(APIView):
    
    def get(self, request, id=None):
        if id:
            query = Issue.objects.select_related('reporter') \
                        .select_related('assignee').select_related('projct').get(pk=id)
            many = False
        else:
            query = Issue.objects.select_related('reporter') \
                        .select_related('assignee').select_related('projct').all()
            many = True
        serializer = IssueSerializer(query, many=many)
        
        return Response(serializer.data)
        
    def post(self, request):
        # TODO: Hardcoded for now. remove once auth finished.
        data = {'reporter': 2}
        data.update(request.data)
        serializer = IssueListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
            
    def delete(self, request, id):
        try:
            issue = Issue.objects.get(id=id)
        except ObjectDoesNotExist:
            raise response.Http404("Issue not found.")
            
        issue.delete()
        return Response(status=204)

    def put(self, request, id):
        try:
            issue = Issue.objects.get(id=id)
        except ObjectDoesNotExist:
            raise response.Http404("Issue not found.")
            
        serializer = IssueListSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
        