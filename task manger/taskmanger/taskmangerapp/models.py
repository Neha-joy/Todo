from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('team_lead', 'Team Lead'),
        ('team_member', 'Team Member'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='team_member')

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, related_name='created_projects', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, related_name='assigned_projects', on_delete=models.CASCADE)

class Task(models.Model):
    STATUS_CHOICES = (
        ('to_do', 'To-Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_do')
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, related_name='tasks', on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, related_name='created_tasks', on_delete=models.CASCADE)