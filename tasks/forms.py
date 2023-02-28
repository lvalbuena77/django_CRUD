from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm): # formulario para crear una tarea 
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']