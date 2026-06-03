import os
import zipfile
import tempfile
import shutil
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.gis.gdal import DataSource
from django.core.serializers import serialize
from .models import EmpreendimentoEolico

# 1. FUNÇÃO DE UPLOAD
def upload_shapefile(request):
    if request.method == 'POST':
        arquivo_zip = request.FILES.get('arquivo_zip')
        if not arquivo_zip:
            return HttpResponse("Nenhum arquivo enviado.")

        temp_dir = tempfile.mkdtemp()
        try:
            zip_path = os.path.join(temp_dir, arquivo_zip.name)
            with open(zip_path, 'wb+') as destination:
                for chunk in arquivo_zip.chunks():
                    destination.write(chunk)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            shp_file = None
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.shp'):
                        shp_file = os.path.join(root, file)
                        break
                if shp_file:
                    break

            if not shp_file:
                return HttpResponse("Erro: Não encontrei nenhum arquivo .shp.")

            ds = DataSource(shp_file)
            layer = ds[0] 
            colunas_shape = layer.fields
            sucesso_count = 0
            
            for feature in layer:
                geom = feature.geom.geos 
                if geom.srid is None:
                    geom.srid = 31984
                elif geom.srid != 31984:
                    geom.transform(31984)

                nome_encontrado = "Nome Não Identificado"
                for opcao in ['Nome', 'NOME', 'nome', 'NM_EMPREEN']:
                    if opcao in colunas_shape:
                        nome_encontrado = str(feature.get(opcao))
                        break

                EmpreendimentoEolico.objects.create(nome_parque=nome_encontrado, geom=geom)
                sucesso_count += 1

            return HttpResponse(f"SUCESSO ABSOLUTO! {sucesso_count} parques salvos.")
        except Exception as e:
            return HttpResponse(f"Deu erro: {str(e)}")
        finally:
            shutil.rmtree(temp_dir)
    return render(request, 'upload.html')


# 2. FUNÇÃO DA TELA INICIAL
def pagina_inicio(request):
    eolicas = EmpreendimentoEolico.objects.all()
    total_eolicas = eolicas.count()
    
    # Voltamos para o formato simples que envia os dados corretamente!
    eolicas_geojson = serialize('geojson', eolicas, geometry_field='geom', fields=('nome_parque',))
    
    return render(request, 'inicio.html', {
        'total_eolicas': total_eolicas,
        'eolicas_geojson': eolicas_geojson 
    })


# 3. FUNÇÃO DO MAPA INTERATIVO
def pagina_mapa(request):
    eolicas = EmpreendimentoEolico.objects.all()
    eolicas_geojson = serialize('geojson', eolicas, geometry_field='geom', fields=('nome_parque',))
    
    return render(request, 'mapa_interativo.html', {'eolicas_geojson': eolicas_geojson})