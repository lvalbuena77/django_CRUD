from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
                return HttpResponse('Usuario registrado con éxito')
            except:
                return render (request, 'signup.html', {'form': UserCreationForm, 
                                                        'error': 'El usuario ya existe'})
            
        else:
            # mostrar mensaje de error
            return render (request, 'signup.html', {'form': UserCreationForm,
                                                    'error': 'Las contraseñas no coinciden'})                                                    
