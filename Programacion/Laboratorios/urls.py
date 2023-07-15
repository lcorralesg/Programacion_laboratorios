from django.urls import path
from .import views

app_name = 'Laboratorios'

urlpatterns = [
    path('',views.index, name='index'),
    path('listado',views.progLab, name='labs'),
    path('registrar',views.registrar, name='registrar'),
    path('editar/<id>',views.editar_datos, name='editar'),
    path('editar',views.editar, name='actualizar'),
    path('eliminar/<id>',views.eliminar, name='eliminar'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='logout_view'),
    path('pdf/', views.Pdf.as_view(), name='pdf'),
]