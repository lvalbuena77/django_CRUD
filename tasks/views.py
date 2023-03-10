from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render (request, 'home.html')

def signup(request): # formulario de registro de usuario 
    
    if request.method == 'GET': # si el usuario esta solicitando la pagina
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        # crear nuevo usuario
        if request.POST['password1'] == request.POST['password2']:
            #Registrar usuario
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user) # iniciar sesion
                return redirect('tasks') # redireccionar a la pagina de tareas
            except IntegrityError:  # si el usuario ya existe mostrar mensaje de error          
                return render (request, 'signup.html', {'form': UserCreationForm, 
                                                        'error': 'El usuario ya existe'})
            
        else:
            # mostrar mensaje de error
            return render (request, 'signup.html', {'form': UserCreationForm,
                                                    'error': 'Las contraseñas no coinciden'})
            
@login_required # solo se puede acceder a esta pagina si el usuario esta autenticado          
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) # filtrar tareas por usuario y por fecha de completado
    return render (request, 'tasks.html', {'tasks': tasks})

@login_required # solo se puede acceder a esta pagina si el usuario esta autenticado
def tasks_completed(request): # mostrar tareas completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') # filtrar tareas por usuario y por fecha de completado
    return render (request, 'tasks_completed.html', {'tasks': tasks})
    
@login_required # solo se puede acceder a esta pagina si el usuario esta autenticado
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm})
    else:
        try: # si el usuario esta creando una tarea 
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError: # si el usuario no ha introducido datos mostrar mensaje de error para que no caiga el servidor
            return render(request, 'create_task.html', {'form': TaskForm,
                                                        'error': 'Datos incorrectos'})
            
@login_required # solo se puede acceder a esta pagina si el usuario esta autenticado            
def task_detail(request, task_id): # actualizar tarea 
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form}) # mostrar formulario con los datos de la tarea    
    else:
        try: # si el usuario esta actualizando una tarea
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task) # actualizar tarea. Se le pasa el método POST para que guarde los cambios
            form.save()
            return redirect ('tasks')
        except ValueError: # si el usuario no ha introducido datos mostrar mensaje de error para que no caiga el servidor
            return render(request, 'task_detail.html', {'task': task}, {'form': form,
                                                        'error': 'Error actualizando tarea'})

@login_required # solo se puede acceder a esta pagina si el usuario esta autenticado            
def complete_task(request, task_id): 
    task = get_object_or_404(Task, pk=task_id, user=request.user) # filtrar tarea por id y por usuario 
    if request.method == 'POST': # si el usuario esta completando una tarea. Si es POST es porque se ha pulsado el boton de completar tarea
        task.datecompleted = timezone.now() # actualizar fecha de completado si el usuario ha pulsado el boton de completar tarea
        task.save() # guardar cambios
        return redirect('tasks') # redireccionar a la pagina de tareas 

@login_required # solo se puede acceder a esta pagina si el usuario esta autenticado   
def delete_task(request, task_id): # eliminar tarea
    task = get_object_or_404(Task, pk=task_id, user=request.user) # filtrar tarea por id y por usuario 
    if request.method == 'POST': # si el usuario esta eliminando una tarea. Si es POST es porque se ha pulsado el boton de eliminar tarea
        task.delete() # eliminar tarea
        return redirect('tasks') # redireccionar a la pagina de tareas

def signout(request): # cerrar sesion
    logout(request)
    return redirect('home')

def signin(request): # formulario de inicio de sesion 
    if request.method == 'GET': # si el usuario esta solicitando la pagina de inicio de sesion 
        return render(request, 'signin.html', {'form': AuthenticationForm})    
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None: # si el usuario no existe mostrar mensaje de error 
            return render(request, 'signin.html', {'form': AuthenticationForm,
                                                   'error': 'El usuario o contraseña son incorrectos'})
        else: # si el usuario existe iniciar sesion y redireccionar a la pagina de tareas 
            login(request, user)
            return redirect('tasks')
        
