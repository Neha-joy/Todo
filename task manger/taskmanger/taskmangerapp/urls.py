from django.urls import path
from .views import register, login_view, logout_view, create_project, edit_project, delete_project, project_list, project_detail, create_task, edit_task, delete_task, view_tasks, update_task_status, dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('projects/', project_list, name='project_list'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/edit/<int:project_id>/', edit_project, name='edit_project'),
    path('projects/delete/<int:project_id>/', delete_project, name='delete_project'),
    path('projects/<int:project_id>/', project_detail, name='project_detail'),
    path('projects/<int:project_id>/tasks/create/', create_task, name='create_task'),
    path('tasks/edit/<int:task_id>/', edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', delete_task, name='delete_task'),
    path('tasks/', view_tasks, name='view_tasks'),
    path('tasks/update/<int:task_id>/', update_task_status, name='update_task_status'),
]