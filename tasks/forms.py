
from .models import Task
from django import forms

class TaskForm(forms.ModelForm): # formulario para crear una tarea 
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la tarea'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la tarea'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})
            
        }