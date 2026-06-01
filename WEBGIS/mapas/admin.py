from django.contrib.gis import admin
from .models import EmpreendimentoEolico

@admin.register(EmpreendimentoEolico)
class EmpreendimentoEolicoAdmin(admin.GISModelAdmin):
    list_display = ('nome_parque', 'status_operacional', 'capacidade_mw')
    search_fields = ('nome_parque',)