from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model): # crea una tabla en la base de datos 
    title = models.CharField(max_length=100) # campo de texto
    description = models.TextField(blank=True) # campo de texto largo
    created = models.DateTimeField(auto_now_add=True) # campo de fecha y hora 
    datecompleted = models.DateTimeField(null=True, blank=True) # campo de fecha y hora
    important = models.BooleanField(default=False) # campo booleano 
    user = models.ForeignKey(User, on_delete=models.CASCADE) # campo de relacion con la tabla User. Si se elimina un usuario se eliminan sus tareas
    
    def __str__(self): # metodo que devuelve el titulo de la tarea 
        return self.title + ' - by ' + self.user.username
