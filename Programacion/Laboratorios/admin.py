from django.contrib import admin
from .models import Laboratorio, Curso, Curso_dictado, Especialidad, Profesor, Programacion_laboratorio

# Register your models here.

@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad_alumnos', 'cantidad_equipos', 'herramientas')

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'creditos', 'especialidad')

@admin.register(Curso_dictado)
class Curso_dictadoAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'curso')

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'dni', 'direccion', 'telefono', 'email')

@admin.register(Programacion_laboratorio)
class Programacion_laboratorioAdmin(admin.ModelAdmin):
    list_display = ('laboratorio', 'curso_dictado', 'fecha', 'hora_inicio', 'hora_fin')
