# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


class Archivo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario que subió el archivo
    nombre = models.CharField(max_length=255)  # Campo para el nombre
    descripcion = models.TextField()  # Campo para la descripción
    archivo = models.FileField(upload_to='archivos/')  # Campo para el archivo cargado
    fecha_subida = models.DateTimeField(auto_now_add=True)  # Fecha y hora de subida

    def __str__(self):
        return self.nombre
    

# Señal para eliminar el archivo del almacenamiento al eliminar la instancia
@receiver(post_delete, sender=Archivo)
def eliminar_archivo(sender, instance, **kwargs):
    if instance.archivo:
        instance.archivo.delete(False)  # False evita guardar el modelo nuevamente


# Señal para eliminar el archivo anterior antes de actualizar
@receiver(pre_save, sender=Archivo)
def actualizar_archivo(sender, instance, **kwargs):
    if not instance.pk:  # Si es una nueva instancia, no hace nada
        return

    try:
        # Obtener la instancia previa antes de actualizar
        old_instance = Archivo.objects.get(pk=instance.pk)
        # Si el archivo anterior es diferente al nuevo, eliminar el anterior
        if old_instance.archivo and old_instance.archivo != instance.archivo:
            old_instance.archivo.delete(save=False)  # Elimina el archivo anterior
    except Archivo.DoesNotExist:
        pass  # Si no existe la instancia previa, no hay nada que eliminar