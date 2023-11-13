from django.urls import path
from .views import TaskListView,AddTaskView,EditTaskView,DeleteTaskView



urlpatterns = [
    path('task_list/',TaskListView.as_view(),name='task_list'),
    path('add-task/',AddTaskView.as_view(),name='add_task'),
    path('edit-task/<int:pk>/',EditTaskView.as_view(),name='edit_task'),
    path('delete-task/<int:pk>/',DeleteTaskView.as_view(),name='delete_task'),
    
]