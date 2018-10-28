from rest_framework import serializers
from .models import TodoItem

class TodoItemSerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = TodoItem
        fields = ('id', 'title', 'owner', 'complete')

class MarkCompleteSerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.username')
    #title = serializer.ReadOnlyField(source')
    class Meta:
        model = TodoItem
        fields = ('id', 'title', 'owner', 'complete')
