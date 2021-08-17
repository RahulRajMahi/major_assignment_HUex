from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project
from .serializers import ProjectSerializer


class ProjectView(APIView):

    def get(self, request, id=None):
        if id is None:
            query = Project.objects.all()
            many = True
        else:
            query = Project.objects.get(id=id)
            many = False

        serializer = ProjectSerializer(query, many=many)

        return Response(serializer.data)
    
    def post(self, request):
        # TODO: Hardcoded for now. remove once auth finished.
        data = {"creator": 2}
        data.update(request.data)
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, id):
        try:
            project = Project.objects.get(id=id)
        except ObjectDoesNotExist:
            raise response.Http404("Project not found.")
            
        project.delete()
        return Response(status=204)

    def put(self, request, id):
        try:
            project = Project.objects.get(id=id)
        except ObjectDoesNotExist:
            raise response.Http404("Project not found.")
            
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
        
        