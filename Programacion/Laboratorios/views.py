from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib import messages
from datetime import datetime, timedelta
from django.views import View
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import requests
from datetime import datetime
from .utils import obtener_datos_clima

# Create your views here.

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'El nombre de usuario debe ser menor a 150 caracteres y no puede contener caracteres especiales'
        self.fields['password1'].help_text = 'La contraseña debe tener al menos 3 caracteres'
        self.fields['password2'].help_text = 'La contraseña debe tener al menos 3 caracteres'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Laboratorios:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'autenticacion/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/listado')
    else:
        form = AuthenticationForm()
    return render(request, 'autenticacion/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

#PROGRAMACION LABORATORIOS

def index(request):
    # Recoger los ultimos 5 laboratorios programados
    listadoProgLabs = Programacion_laboratorio.objects.all().order_by('-id')
    laboratorios = Laboratorio.objects.all()
    cursos_dictados = Curso_dictado.objects.all()
    temperatura, descripcion, fecha_hora_actual = obtener_datos_clima()
    if request.method == 'POST':
        # Obtener los datos del formulario
        laboratorio = request.POST.get('laboratorio')
        semana = request.POST.get('semana')

        # Obtener la fecha de inicio de la semana seleccionada
        fecha_inicio = datetime.strptime(semana + '-1', '%Y-W%W-%w').date()

        # Obtener la fecha de fin de la semana seleccionada
        fecha_fin = fecha_inicio + timedelta(days=6)

        # Realizar la consulta a la base de datos
        programaciones = Programacion_laboratorio.objects.filter(
            Q(laboratorio=laboratorio) &
            (Q(fecha__range=(fecha_inicio, fecha_fin)))).order_by('fecha')
        
        dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Cambiar el formato de la fecha a dia
        for programacion in programaciones:
            programacion.fecha = programacion.fecha.strftime('%A')

        # Obtener el nombre del laboratorio seleccionado
        laboratorio = Laboratorio.objects.get(id=laboratorio)
        
        context = {
            "labs": listadoProgLabs,
            "laboratorios": laboratorios,
            "cursos_dictados": cursos_dictados,
            "programaciones": programaciones,
            "laboratorio": laboratorio,
            "semana": semana,
            "dias_semana": dias_semana,
            "temperatura": temperatura,
            "descripcion": descripcion,
            "fecha_hora_actual": fecha_hora_actual
        }
        return render(request, 'index.html', context)
    else:
        context = {
            "labs": listadoProgLabs,
            "laboratorios": laboratorios,
            "cursos_dictados": cursos_dictados,
            "temperatura": temperatura,
            "descripcion": descripcion,
            "fecha_hora_actual": fecha_hora_actual
        }
        return render(request, "index.html", context)

@login_required(login_url='Laboratorios:login')
def progLab(request):
    listadoProgLabs = Programacion_laboratorio.objects.all()
    laboratorios = Laboratorio.objects.all()
    cursos_dictados = Curso_dictado.objects.all()
    temperatura, descripcion, fecha_hora_actual = obtener_datos_clima()
    return render(request, "listado.html", {"labs": listadoProgLabs, "laboratorios": laboratorios, "cursos_dictados": cursos_dictados, "temperatura": temperatura, "descripcion": descripcion, "fecha_hora_actual": fecha_hora_actual})

@login_required(login_url='Laboratorios:login')
def registrar(request):
    laboratorio_id = request.POST["txtlaboratorio"]
    curso_dictado_id = request.POST["txtcurso_dictado"]
    fecha = request.POST["txtfecha"]
    hora_inicio = request.POST["txthora_inicio"]
    hora_fin = request.POST["txthora_fin"]

    laboratorio = Laboratorio.objects.get(id=laboratorio_id)
    curso_dictado = Curso_dictado.objects.get(id=curso_dictado_id)

    if Programacion_laboratorio.objects.filter(
        Q(laboratorio=laboratorio) &
        (Q(fecha=fecha) & (Q(hora_inicio__range=(hora_inicio, hora_fin)) | Q(hora_fin__range=(hora_inicio, hora_fin))))).exists():
        messages.error(request, "Ya existe una programación para el laboratorio en el rango de fechas y horas especificado.")
    else:
        lab_programado = Programacion_laboratorio(
        laboratorio=laboratorio,
        curso_dictado=curso_dictado,
        fecha=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin)
        lab_programado.save()
        messages.success(request, "Programación de laboratorio registrada correctamente.")
    return redirect('/listado')

@login_required(login_url='Laboratorios:login')
def editar_datos(request,id):
    datos=Programacion_laboratorio.objects.get(id=id)

    codigo_lab=datos.laboratorio.id
    laboratorio=Laboratorio.objects.get(pk=codigo_lab)
    laboratorioListado=Laboratorio.objects.exclude(pk=codigo_lab)

    codigo_curso=datos.curso_dictado.id
    curso_dictado=Curso_dictado.objects.get(pk=codigo_curso)
    cursoListado=Curso_dictado.objects.exclude(pk=codigo_curso)
    
    listadoProgLabs = Programacion_laboratorio.objects.all()
    laboratorios = Laboratorio.objects.all()
    cursos_dictados = Curso_dictado.objects.all()

    context={
        'datos':datos,
        'laboratorio':laboratorio,
        'laboratorios':laboratorioListado,
        'curso_dictado':curso_dictado,
        'cursos':cursoListado,
        "labs": listadoProgLabs,
        "laboratorios": laboratorios,
        "cursos_dictados": cursos_dictados
    }
    return render(request,"editar.html",context)

@login_required(login_url='Laboratorios:login')
def editar(request):
    id=request.POST["idpro"]
    laboratorio_id=request.POST["txtlaboratorio"]
    curso_dictado_id = request.POST["txtcurso_dictado"]
    fecha = request.POST["txtfecha"]
    hora_inicio = request.POST["txthora_inicio"]
    hora_fin = request.POST["txthora_fin"]

    laboratorio = Laboratorio.objects.get(id=laboratorio_id)
    curso_dictado = Curso_dictado.objects.get(id=curso_dictado_id)

    if Programacion_laboratorio.objects.filter(
        Q(laboratorio=laboratorio) &
        (Q(fecha=fecha) & (Q(hora_inicio__range=(hora_inicio, hora_fin)) | Q(hora_fin__range=(hora_inicio, hora_fin))))).exclude(id=id).exists():
        messages.error(request, "Ya existe una programación para el laboratorio en el rango de fechas y horas especificado.")
    else:
        program = Programacion_laboratorio.objects.get(id=id)
        program.laboratorio = laboratorio
        program.curso_dictado = curso_dictado
        program.fecha = fecha
        program.hora_inicio = hora_inicio
        program.hora_fin = hora_fin
        program.save()
        messages.success(request, "Programación de laboratorio editada correctamente.")
    
    return redirect('/listado')

@login_required(login_url='Laboratorios:login')
def eliminar(request,id):
    program=Programacion_laboratorio.objects.get(id=id)
    program.delete()
    return redirect('/listado')

class Pdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf.html')
        context = {'labs': Programacion_laboratorio.objects.all()}
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
        pisaStatus = pisa.CreatePDF(html, dest=response)

        if pisaStatus.err:
            return HttpResponse("We had some errors <pre>" + html + "</pre>")

        return response
    
def obtener_datos_clima():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Lima&appid=bf7affab900e00c1e1febb54775f9185"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Convertir la temperatura de Kelvin a Celsius
        temperatura_kelvin = data['main']['temp']
        temperatura_celsius = temperatura_kelvin - 273.15
        # Formatear la temperatura a dos decimales
        temperatura_formateada = "{:.2f}".format(temperatura_celsius)
        descripcion = data['weather'][0]['description']
        fecha_hora = data['dt']
        # Convertir la fecha y hora en un formato legible
        fecha_hora_actual = datetime.fromtimestamp(fecha_hora).strftime('%Y-%m-%d %H:%M:%S')
        return temperatura_formateada, descripcion, fecha_hora_actual
    else:
        return None, None, None