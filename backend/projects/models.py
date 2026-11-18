from django.db import models
from django.conf import settings

class Project(models.Model):
   user = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE,
       related_name="projects"
   ) 
   
   name = models.CharField(max_length=200)
   
   description = models.TextField(blank=True)
   
   created_at = models.DateTimeField(auto_now_add=True)
   
   updated_at = models.DateTimeField(auto_now=True)
   
   def __str__(self):
       return self.name
   
   
class Category(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="categories"
    )
    
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "name"],
                name="unique_category_per_project"
            )
        ]
    def __str__(self):
        return self.name