import os
import zipfile
import tempfile
import shutil
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.gis.gdal import DataSource
from django.core.serializers import serialize
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET
from django.utils import timezone
from .models import EmpreendimentoEolico
from django.conf import settings

@staff_member_required
def upload_shapefile(request):
    """
    Processa o upload de arquivos compactados (.zip) contendo shapefiles,
    extrai os arquivos espaciais, realiza a leitura da camada vetorial e
    salva os registros de parques eólicos no banco de dados espacial PostGIS.

    Parâmetros:
        request (HttpRequest): O objeto de requisição do Django contendo o arquivo ZIP.

    Retorna:
        HttpResponse: Uma resposta redirecionando com mensagens ou renderizando a página de upload.
    """
    if request.method == 'POST':
        arquivo_zip = request.FILES.get('arquivo_zip')
        if not arquivo_zip:
            messages.error(request, "Nenhum arquivo enviado.")
            return render(request, 'upload.html')

        # Criação de um diretório temporário isolado para extração
        temp_dir = tempfile.mkdtemp()
        try:
            zip_path = os.path.join(temp_dir, arquivo_zip.name)
            with open(zip_path, 'wb+') as destination:
                for chunk in arquivo_zip.chunks():
                    destination.write(chunk)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Busca recursiva pelo arquivo .shp principal
            shp_file = None
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.shp'):
                        shp_file = os.path.join(root, file)
                        break
                if shp_file:
                    break

            if not shp_file:
                messages.error(request, "Erro: Não encontrei nenhum arquivo .shp.")
                return render(request, 'upload.html')

            # Leitura do Shapefile com a biblioteca GDAL/OGR
            ds = DataSource(shp_file)
            layer = ds[0] 
            colunas_shape = layer.fields
            sucesso_count = 0
            
            # Carrega a malha de municípios para cruzamento espacial off-line
            caminho_mun = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'geojson', 'geojs-24-mun.json')
            municipalities = []
            try:
                with open(caminho_mun, 'r', encoding='utf-8') as f:
                    mun_data = json.load(f)
                from django.contrib.gis.geos import GEOSGeometry
                for feature in mun_data['features']:
                    name = feature['properties']['name']
                    geom_mun = GEOSGeometry(json.dumps(feature['geometry']))
                    geom_mun.srid = 4326
                    municipalities.append({'name': name, 'geom': geom_mun})
            except Exception as e:
                pass
            
            for feature in layer:
                # Obtenção da geometria vetorial do elemento
                geom = feature.geom.geos 
                
                # Garantia de sistema de referência espacial UTM 24S (SRID 31984)
                if geom.srid is None:
                    geom.srid = 31984
                elif geom.srid != 31984:
                    geom.transform(31984)

                # Mapeamento do nome do parque a partir de colunas comuns
                nome_encontrado = "Nome Não Identificado"
                for opcao in ['Nome', 'NOME', 'nome', 'NM_EMPREEN']:
                    if opcao in colunas_shape:
                        nome_encontrado = str(feature.get(opcao))
                        break

                # Mapeamento do status a partir de colunas comuns
                status_encontrado = None
                for opcao in ['Status', 'STATUS', 'status', 'STATUS_OPE', 'status_ope', 'Situação', 'SITUACAO', 'situacao']:
                    if opcao in colunas_shape:
                        status_encontrado = str(feature.get(opcao))
                        break

                # Mapeamento da fonte a partir de colunas comuns
                fonte_encontrada = None
                for opcao in ['Fonte', 'FONTE', 'fonte', 'FONTE_DADO', 'fonte_dado', 'Fonte_Dado']:
                    if opcao in colunas_shape:
                        fonte_encontrada = str(feature.get(opcao))
                        break

                # Cruzamento espacial para obter o município
                geom_4326 = geom.clone()
                geom_4326.transform(4326)
                nome_municipio = None
                for mun in municipalities:
                    if mun['geom'].contains(geom_4326):
                        nome_municipio = mun['name']
                        break

                # Persistência do registro espacial no banco de dados
                EmpreendimentoEolico.objects.create(
                    nome_parque=nome_encontrado,
                    municipio=nome_municipio,
                    status_operacional=status_encontrado,
                    status=status_encontrado,
                    fonte_dado=fonte_encontrada,
                    fonte=fonte_encontrada,
                    geom=geom
                )
                sucesso_count += 1

            messages.success(request, 'Shapefile importado e processado com sucesso!')
            return redirect('admin:mapas_empreendimentoeolico_changelist')
        except Exception as e:
            messages.error(request, f"Deu erro: {str(e)}")
            return render(request, 'upload.html')
        finally:
            # Garante que os arquivos temporários criados sejam apagados
            shutil.rmtree(temp_dir)
    return render(request, 'upload.html')


def pagina_inicio(request):
    """
    Renderiza a página inicial do portal, calculando o total de torres
    eólicas cadastradas e serializando as geometrias em formato GeoJSON
    para visualização cartográfica interativa.

    Parâmetros:
        request (HttpRequest): O objeto de requisição do Django.

    Retorna:
        HttpResponse: A página HTML 'inicio.html' renderizada com o total de eólicas
                      e os dados em GeoJSON.
    """
    eolicas = EmpreendimentoEolico.objects.all()
    total_eolicas = eolicas.count()
    
    # Busca a última torre inserida para pegar a data de atualização
    ultima_torre = eolicas.order_by('-id').first()
    ultima_atualizacao = ultima_torre.data_registro if ultima_torre and hasattr(ultima_torre, 'data_registro') else timezone.now()
    
    # Serializa os objetos de parque eólico em GeoJSON com suas geometrias
    eolicas_geojson = serialize('geojson', eolicas, geometry_field='geom', fields=('nome_parque', 'status_operacional', 'capacidade_mw', 'fonte_dado'))
    
    return render(request, 'inicio.html', {
        'total_eolicas': total_eolicas,
        'eolicas_geojson': eolicas_geojson,
        'ultima_atualizacao': ultima_atualizacao
    })


def pagina_mapa(request):
    """
    Renderiza a página exclusiva do mapa interativo WebGIS, fornecendo
    a base de dados espacial de eólicas serializada no formato GeoJSON.

    Parâmetros:
        request (HttpRequest): O objeto de requisição do Django.

    Retorna:
        HttpResponse: A página HTML 'mapa_interativo.html' renderizada com os dados do mapa.
    """
    torres = EmpreendimentoEolico.objects.all()
    qtd_torres = torres.count()
    
    # Busca a última torre inserida para pegar a data de atualização
    ultima_torre = torres.order_by('-id').first()
    ultima_atualizacao = ultima_torre.data_registro if ultima_torre and hasattr(ultima_torre, 'data_registro') else timezone.now()
    
    eolicas_geojson = serialize('geojson', torres, geometry_field='geom', fields=('nome_parque', 'status_operacional', 'capacidade_mw', 'fonte_dado'))
    
    context = {
        'eolicas_geojson': eolicas_geojson,
        'qtd_torres': qtd_torres,
        'ultima_atualizacao': ultima_atualizacao,
    }
    return render(request, 'mapa_interativo.html', context)


def api_eolicas_geojson(request):
    eolicas = EmpreendimentoEolico.objects.all()
    geojson_data = serialize('geojson', eolicas, geometry_field='geom')
    return HttpResponse(geojson_data, content_type='application/json')


def lista_downloads(request):
    """
    View responsável por escanear o diretório de mídias e listar 
    todos os pacotes Shapefile compactados disponíveis para download.
    """
    diretorio_downloads = os.path.join(settings.MEDIA_ROOT, 'downloads')
    arquivos_disponiveis = []
    
    if os.path.exists(diretorio_downloads):
        for arquivo in os.listdir(diretorio_downloads):
            if arquivo.endswith('.zip'):
                # Formata o nome do arquivo para exibição (ex: torres_currais_novos.zip -> Currais Novos)
                nome_exibicao = arquivo.replace('torres_', '').replace('.zip', '').replace('_', ' ').title()
                
                arquivos_disponiveis.append({
                    'arquivo_nome': arquivo,
                    'municipio': nome_exibicao,
                    'url': f"{settings.MEDIA_URL}downloads/{arquivo}"
                })
                
    # Ordena a lista alfabeticamente pelo nome do município
    arquivos_disponiveis = sorted(arquivos_disponiveis, key=lambda x: x['municipio'])
    
    return render(request, 'mapas/downloads.html', {'downloads': arquivos_disponiveis})