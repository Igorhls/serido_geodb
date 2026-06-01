from django.contrib import admin
from django.urls import path, include # <-- adicione o include aqui

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mapas/', include('mapas.urls')), # <-- adicione esta linha
]