from django.urls import path
from .Crud.Iglesia import create_iglesia,list_iglesias
from .Crud.Inscricion import *
urlpatterns = [
    path('iglesia/crear/', create_iglesia), 
    path('iglesia/listar/', list_iglesias),

    path('Inscripcion/crear/', create_inscrito), 
    path('Inscripcion/listar/', list_inscritos), 
    path('Inscripcion/cupo/', cupo_inscritos), 
    path('Inscripcion/confirmar/', confirmar_inscrito),
]
