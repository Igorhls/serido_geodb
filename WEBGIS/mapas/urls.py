from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_shapefile, name='upload_shapefile'),
    path('', views.pagina_inicio, name='pagina_inicio'),       # <-- Rota da Tela Inicial
    path('mapa/', views.pagina_mapa, name='pagina_mapa'),      # <-- Rota do Mapa WebGIS
    path('api/eolicas/', views.api_eolicas_geojson, name='api_eolicas'),
]