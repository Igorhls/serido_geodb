from django.contrib.gis import admin
from .models import EmpreendimentoEolico

# Customização do cabeçalho e título do painel administrativo do Django
admin.site.site_header = "Painel Administrativo - BDG Seridó Renovável"
admin.site.site_title = "BDG Seridó"
admin.site.index_title = "Gerenciamento de Dados Geoespaciais"
admin.site.site_url = '/mapas/'

@admin.register(EmpreendimentoEolico)
class EmpreendimentoEolicoAdmin(admin.GISModelAdmin):
    list_display = ('id', 'nome_parque', 'status_operacional', 'capacidade_mw', 'fonte_dado')
    search_fields = ('nome_parque',)
    list_filter = ('status_operacional', 'fonte_dado')
    
    fieldsets = (
        ("Dados Principais", {
            'fields': ('nome_parque', 'fonte_dado')
        }),
        ("Dados Técnicos", {
            'fields': ('capacidade_mw', 'status_operacional', 'data_operacao')
        }),
        ("Dados Espaciais", {
            'fields': ('geom',)
        }),
    )