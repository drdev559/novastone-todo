from django.db import models
from django.contrib.auth.models import User

class TodoItem(models.Model):
    title = models.CharField(max_length=160, 
                             blank=False)
    owner = models.ForeignKey(User,
                             related_name='todoitems',
                             on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)


    