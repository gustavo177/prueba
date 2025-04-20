from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Archivo

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    
def login_view(request):
    mensaje_error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome', user_id=user.id)  # Redirige al ID del usuario
        else:
            mensaje_error = "Nombre de usuario o contraseña incorrectos."
    return render(request, 'login.html', {'mensaje_error': mensaje_error})

def logout_view(request):
    logout(request)
    return redirect('/login/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def welcome(request, user_id):

    archivos_usuario = Archivo.objects.filter(usuario__id=user_id)  # Obtén todos los archivos del usuario con ID 2
    user = get_object_or_404(User, id=user_id)  # Obtiene el usuario por ID


    if request.method == 'POST':

        archivo_id = request.POST.get('archivo_id_actualizando')
        if archivo_id:
            archivo = get_object_or_404(Archivo, id=archivo_id, usuario=user)
            archivo.nombre = request.POST.get('nombre')
            archivo.descripcion = request.POST.get('descripcion')
            if 'archivo' in request.FILES:  # Verifica si se subió un archivo nuevo
                archivo.archivo.delete()  # Elimina el archivo anterior
                archivo.archivo = request.FILES['archivo']  # Substituye con el nuevo archivo
            archivo.save()  # Guarda los cambios en la base de datos
            return render(request, 'welcome.html', {
                'username': user.username,
                'user_id': user.id,
                'archivos_usuario': Archivo.objects.filter(usuario__id=user_id),  # Lista actualizada
                'success_message': 'Archivo actualizado correctamente.'
            })

         # Verificar si se envió una solicitud para actualizar un archivo
        read_id = request.POST.get('update_id')
        if read_id:
            archivo = get_object_or_404(Archivo, id=read_id, usuario=user)
            return render(request, 'update.html', {
                'user_id': user_id,
                'archivo': archivo,  # Pasamos el objeto archivo completo
                'success_message': 'Leyendo archivo.'
            })

        # Verificar si se envió una solicitud para eliminar un archivo
        read_id = request.POST.get('read_id')
        if read_id:
            archivo = get_object_or_404(Archivo, id=read_id, usuario=user)
            return render(request, 'read.html', {
                'user_id': user_id,
                'archivo': archivo,  # Pasamos el objeto archivo completo
                'success_message': 'Leyendo archivo.'
            })


        # Verificar si se envió una solicitud para eliminar un archivo
        delete_id = request.POST.get('delete_id')
        if delete_id:
            archivo = get_object_or_404(Archivo, id=delete_id, usuario=user)  # Asegurarse de que el archivo pertenece al usuario
            archivo.archivo.delete()  # Elimina el archivo del sistema de archivos
            archivo.delete()  # Elimina el registro de la base de datos
            return render(request, 'welcome.html', {
                'username': user.username,
                'user_id': user.id,
                'archivos_usuario': Archivo.objects.filter(usuario__id=user_id),
                'success_message': 'Archivo eliminado correctamente.'
            })
        


        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        archivo = request.FILES.get('archivo')

        if archivo:
            # Guardar el archivo en el modelo
            archivo_obj = Archivo.objects.create(
                usuario=user,
                nombre=nombre,
                descripcion=descripcion,
                archivo=archivo
            )

            

            return render(request, 'welcome.html', {
                'username': user.username,  # Muestra el nombre de usuario
                'user_id': user.id,  # Pasa el ID del usuario
                'success_message': 'Archivo subido correctamente.',
                'archivos_usuario': archivos_usuario
            })

    return render(request, 'welcome.html', {'username': user.username, 'user_id': user.id, 'archivos_usuario': archivos_usuario})


