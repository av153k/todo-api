from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Tasks
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import status
# Create your views here.

"""
Api Overview
"""


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List': '/getAllTasks/',
        'Detail View': '/getTaskById/<taskId>/',
        'Create': '/createTasks/',
        'Update': '/updateTask/<taskId>/',
        'Delete': '/deleteTask/<taskId>/',
        'ToggleCompleteStatus': '/toggleCompleteStatus/<taskId>'
    }
    return Response(api_urls)


@api_view(['GET'])
def task_list(request):
    tasks = Tasks.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def task_detail(request, pk):
    task = Tasks.objects.get(id=pk)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def task_update(request, pk):
    task = Tasks.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)
    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def task_create(request):
    """
    ...
    parameters:
    - name: body
      description: JSON body.
      required: true
      paramType: body
      pytype: RequestSerializer
    """
    serializer = TaskSerializer(data=request.data)
    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def toggle_complete_status(request, pk):
    task = Tasks.objects.get(id=pk)
    data = model_to_dict(task)
    task_completed = False if task.completed == True else True
    data['completed'] = task_completed
    serializer = TaskSerializer(instance=task, data=data)
    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)


class TasksByUserIdApiView(ListAPIView):
    permissions_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    queryset = Tasks.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.kwargs['user_id'])
