from rest_framework import viewsets
from .serializers import TaskSerializer
from .models import Tasks

class TaskViewsets(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer