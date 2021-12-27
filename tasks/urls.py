from django.urls import path
from . import views


urlpatterns = [
    # path('docs', views.api_overview, name="apiOverview"),
    path('getAllTasks', views.task_list, name="getAllTasks"),
    path('getTaskById/<str:pk>', views.task_detail, name="getTaskById"),
    path('updateTask/<str:pk>', views.task_update, name="updateTask"),
    path('createTask', views.task_create, name="createTask"),
    path('toggleCompleteStatus/<str:pk>',
         views.toggle_complete_status, name="toggleCompleteStatus"),
    path('tasksByUserId/<str:user_id>', views.TasksByUserIdApiView.as_view()),
]
