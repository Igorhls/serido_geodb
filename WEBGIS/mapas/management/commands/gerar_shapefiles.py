import os
import zipfile
import shapefile
from django.core.management.base import BaseCommand
from django.conf import settings
from mapas.models import EmpreendimentoEolico

class Command(BaseCommand):
    help = 'Gera pacotes Shapefile compactados em ZIP divididos por município de forma otimizada'

    def handle(self, *args, **options):
        # Define o diretório de destino usando caminhos relativos
        output_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')
        os.makedirs(output_dir, exist_ok=True)

        # Definição WKT para SIRGAS 2000 / UTM Zone 24S (EPSG: 31984)
        prj_wkt = (
            'PROJCS["SIRGAS_2000_UTM_Zone_24S",GEOGCS["GCS_SIRGAS_2000",'
            'DATUM["D_SIRGAS_2000",SPHEROID["GRS_1980",6378137.0,298.257222101]],'
            'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],'
            'PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],'
            'PARAMETER["False_Northing",10000000.0],PARAMETER["Central_Meridian",-39.0],'
            'PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],'
            'UNIT["Meter",1.0]]'
        )
        # Componentes do Shapefile
        componentes = ['.shp', '.shx', '.dbf', '.prj']

        self.stdout.write("Processando feições globais (Todos os Municípios)...")
        caminho_base_todos = os.path.join(output_dir, "torres_00_todos_os_municipios")
        torres_todas = EmpreendimentoEolico.objects.all()

        with shapefile.Writer(caminia_base_todos := caminho_base_todos, shapeType=shapefile.POINT) as shp:
            shp.field('NOME', 'C', 100)
            shp.field('MUNICIPIO', 'C', 50)
            shp.field('FONTE', 'C', 100)
            shp.field('STATUS', 'C', 50)
            for torre in torres_todas:
                if torre.geom:
                    shp.point(torre.geom.x, torre.geom.y)
                    shp.record(
                        torre.nome_parque or '',
                        torre.municipio or '',
                        torre.fonte or '',
                        torre.status or ''
                    )

        with open(f"{caminho_base_todos}.prj", "w", encoding='utf-8') as prj:
            prj.write(prj_wkt)

        with zipfile.ZipFile(f"{caminho_base_todos}.zip", 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for ext in componentes:
                arquivo_comp = caminho_base_todos + ext
                if os.path.exists(arquivo_comp):
                    zip_file.write(arquivo_comp, arcname=f"torres_00_todos_os_municipios{ext}")
                    os.remove(arquivo_comp)

        self.stdout.write(self.style.SUCCESS("Sucesso: torres_00_todos_os_municipios.zip gerado."))

        municipios = EmpreendimentoEolico.objects.values_list('municipio', flat=True).distinct()

        for municipio in municipios:
            if not municipio:
                continue

            nome_base = f"torres_{municipio.lower().replace(' ', '_')}"
            caminho_base = os.path.join(output_dir, nome_base)

            self.stdout.write(f"Processando municipio: {municipio}...")

            with shapefile.Writer(caminho_base, shapeType=shapefile.POINT) as shp:
                # Estrutura do .dbf
                shp.field('NOME', 'C', 100)
                shp.field('MUNICIPIO', 'C', 50)
                shp.field('FONTE', 'C', 100)
                shp.field('STATUS', 'C', 50)

                torres = EmpreendimentoEolico.objects.filter(municipio=municipio)

                for torre in torres:
                    if torre.geom:
                        shp.point(torre.geom.x, torre.geom.y)
                        shp.record(
                            torre.nome_parque or '',
                            torre.municipio or '',
                            torre.fonte or '',
                            torre.status or ''
                        )

            # Criação do .prj
            with open(f"{caminho_base}.prj", "w", encoding='utf-8') as prj:
                prj.write(prj_wkt)

            # Compactação
            caminho_zip = f"{caminho_base}.zip"
            
            with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for ext in componentes:
                    arquivo_componente = caminho_base + ext
                    if os.path.exists(arquivo_componente):
                        zip_file.write(arquivo_componente, arcname=nome_base + ext)
                        os.remove(arquivo_componente)

            self.stdout.write(self.style.SUCCESS(f"Sucesso: {nome_base}.zip gerado."))
