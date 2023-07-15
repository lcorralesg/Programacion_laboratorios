from django.db import models

# Create your models here.

class Especialidad(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    creditos = models.IntegerField()
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class Profesor(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    dni = models.CharField(max_length=8)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=9)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre + " " + self.apellidos
    
class Curso_dictado(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.profesor.nombre + " " + self.profesor.apellidos + " " + self.curso.nombre
    
class Laboratorio(models.Model):
    nombre = models.CharField(max_length=50)
    capacidad_alumnos = models.IntegerField()
    cantidad_equipos = models.IntegerField()
    herramientas = models.JSONField()

    def __str__(self):
        return self.nombre
    
class Programacion_laboratorio(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    curso_dictado = models.ForeignKey(Curso_dictado, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()


    