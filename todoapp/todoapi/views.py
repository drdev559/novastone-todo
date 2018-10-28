from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from .serializers import TodoItemSerializer
from .models import TodoItem
from .permissions import IsOwner

class ListView(generics.ListAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    def get_queryset(self, *args, **kwargs):
     return TodoItem.objects.all().filter(owner=self.request.user)

class CreateView(generics.CreateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)



