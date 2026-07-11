from django.contrib.gis.db import models

# Tabela de Eólicas (Pontos)
class EmpreendimentoEolico(models.Model):
    nome_parque = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nome do Parque')
    municipio = models.CharField(max_length=150, null=True, blank=True, verbose_name='Município')
    status_operacional = models.CharField(max_length=100, null=True, blank=True, verbose_name='Status Operacional')
    capacidade_mw = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Capacidade (MW)')
    data_operacao = models.DateField(null=True, blank=True, verbose_name='Data de Operação')
    fonte_dado = models.CharField(max_length=100, null=True, blank=True, verbose_name='Fonte de Dados')
    
    # Novos campos para compatibilidade com a tabela de atributos do QGIS
    fonte = models.CharField(max_length=255, blank=True, null=True, verbose_name="Fonte")
    status = models.CharField(max_length=100, blank=True, null=True, verbose_name="Status")
    
    # O campo mágico espacial! (Ponto com SRC UTM 24S)
    geom = models.PointField(srid=31984, spatial_index=True, verbose_name='Geometria')
    
    # Campo de rastreamento de data de modificação
    atualizado_em = models.DateTimeField(auto_now=True, null=True, verbose_name='Última Atualização')

    class Meta:
        verbose_name = 'Empreendimento Eólico'
        verbose_name_plural = 'Empreendimentos Eólicos'

    def __str__(self):
        return self.nome_parque or "Parque Eólico (Sem nome)"

# Tabela de Solares (Polígonos)
class EmpreendimentoSolar(models.Model):
    nome_usina = models.CharField(max_length=255, null=True, blank=True)
    municipio = models.CharField(max_length=150, null=True, blank=True, verbose_name='Município')
    status_operacional = models.CharField(max_length=100, null=True, blank=True)
    capacidade_mw = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_operacao = models.DateField(null=True, blank=True)
    fonte_dado = models.CharField(max_length=100, null=True, blank=True)
    
    # Novos campos para compatibilidade com a tabela de atributos do QGIS
    fonte = models.CharField(max_length=255, blank=True, null=True, verbose_name="Fonte")
    status = models.CharField(max_length=100, blank=True, null=True, verbose_name="Status")
    
    # O campo mágico espacial! (Polígono com SRC UTM 24S)
    geom = models.PolygonField(srid=31984, spatial_index=True, verbose_name='Geometria')

    def __str__(self):
        return self.nome_usina or "Usina Solar (Sem nome)"