from django.contrib.gis import admin
from django.core.management import call_command
from django.contrib import messages
from .models import EmpreendimentoEolico

# Customização do cabeçalho e título do painel administrativo do Django
admin.site.site_header = "Painel Administrativo - BDG Seridó Renovável"
admin.site.site_title = "BDG Seridó"
admin.site.index_title = "Gerenciamento de Dados Geoespaciais"
admin.site.site_url = '/mapas/'

@admin.register(EmpreendimentoEolico)
class EmpreendimentoEolicoAdmin(admin.GISModelAdmin):
    list_display = ('id', 'nome_parque', 'municipio', 'status_operacional', 'capacidade_mw', 'fonte_dado')
    search_fields = ('nome_parque', 'municipio')
    list_filter = ('municipio', 'status_operacional', 'fonte_dado')
    ordering = ('municipio', 'nome_parque')
    actions = ['atualizar_arquivos_download']

    @admin.action(description='⚙️ Regerar Arquivos ZIP para Download')
    def atualizar_arquivos_download(self, request, queryset):
        try:
            call_command('gerar_shapefiles')
            self.message_user(request, "Todos os arquivos Shapefile foram regerados e atualizados com sucesso na página de downloads!", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Erro ao gerar arquivos: {str(e)}", level=messages.ERROR)
    
    fieldsets = (
        ("Dados Principais", {
            'fields': ('nome_parque', 'municipio', 'fonte_dado')
        }),
        ("Dados Técnicos", {
            'fields': ('capacidade_mw', 'status_operacional', 'data_operacao')
        }),
        ("Dados Espaciais", {
            'fields': ('geom',)
        }),
    )