from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class TaskListCreateView(generics.ListCreateAPIView):
   permission_classes = [IsAuthenticated]
   serializer_class = TaskSerializer
   
   def get_queryset(self):
       return Task.objects.filter(project__user=self.request.user)
   
   
   
#    def get_queryset(self):
#        if project_id:
#             return Task.objects.filter(project_id=project_id)
#        else:
#             return Task.objects.all()

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
   permission_classes = [IsAuthenticated]
   serializer_class = TaskSerializer
   def get_queryset(self):
      return Task.objects.filter(project__user=self.request.user) 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               