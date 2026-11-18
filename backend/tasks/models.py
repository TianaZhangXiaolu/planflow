from django.db import models
from projects.models import Project, Category

class Task(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
        blank=True
    )
    
    title = models.CharField(max_length=200)
    
    description = models.TextField(blank=True)
    
    is_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title