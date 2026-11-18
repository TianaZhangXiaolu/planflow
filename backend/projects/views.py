from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer
#from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

# ListCreateAPIView 操作的是一个资源集合（Collection）
class ProjectListCreateView(generics.ListCreateAPIView):
     # user right
    permission_classes = [IsAuthenticated]
    # queryset:告诉DRF从哪里获取数据
    #queryset = Project.objects.filter(user=self.request.user)
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    # 告诉DRF用什么方式转换数据
    serializer_class = ProjectSerializer
   
    
    # 测试用的用户
    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)
# RetrieveUpdateDestroyAPIView 操作的是一个具体资源（Detail）
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    serializer_class = ProjectSerializer
     
    
    # def get_queryset(self):
    #     return Project.objects.filter(user=self.request.user)
    
# class ProjectCreateView(generics.CreateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
    
# \
    
