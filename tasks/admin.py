from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',) # Este campo es de solo lectura. En él se guarda la fecha y hora de creación de la tarea 
                                # y no se puede modificar desde el panel de administración de Django  

# Register your models here.
admin.site.register (Task, TaskAdmin)