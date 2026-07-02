# BDG Seridó Renovável

Repositório oficial do projeto de pesquisa: **Estudo da construção de um banco de dados geoespacial de energia renovável: vetorização e mapeamento aplicado na Região do Seridó Potiguar.**

Projeto vinculado ao Edital nº 19/2025 - PROPI/RE/IFRN - PIBIC-Af/CNPq.

---

## 🎯 Objetivo

Este projeto visa construir um banco de dados geoespacial vetorial sobre os empreendimentos de energia eólica e solar na Região do Seridó Potiguar (RN).

O objetivo é organizar e disponibilizar gratuitamente dados atualizados e padronizados para pesquisadores, gestores públicos e a comunidade acadêmica, facilitando o planejamento energético e ambiental na região.

---

## 🚀 Funcionalidades do WebGIS

A plataforma possui um portal WebGIS dinâmico e integrado com as seguintes funcionalidades:

1. **Portal Inicial (`/mapas/`)**:
   - Mapa interativo simplificado do Rio Grande do Norte (RN) gerado a partir do cruzamento espacial de municípios com a base de dados em tempo real.
   - **Destaque do Seridó**: A microrregião do Seridó é demarcada no mapa do RN de forma elegante com bordas tracejadas laranja, mantendo a interatividade dos municípios.
   - **Painel de Estatísticas**: Exibição da quantidade total de torres cadastradas (289 atualmente), número de municípios com torres instaladas e a data/hora da **última atualização do banco de dados**.

2. **Mapa Interativo WebGIS (`/mapas/mapa/`)**:
   - Exibição de camadas de dados espaciais (OpenStreetMap padrão e Imagens de Satélite Esri).
   - **Agrupamento Dinâmico (Cluster)**: Visualização de torres individuais ou agrupadas para análise espacial em grandes escalas.
   - **Marcadores Vetoriais SVG**: Torres eólicas representadas por ícones SVG vetoriais realistas em ciano brilhante, com rotor e pás detalhadas.
   - **Popups de Informação**: Dados detalhados de cada torre (Nome do Parque, Situação Operacional, Coordenadas Geográficas de Latitude/Longitude e Fonte do Dado).
   - **Painel de Controle Flutuante**: Caixa de estatísticas moderna em Dark Mode mostrando a quantidade total de torres e o carimbo de data da última sincronização.

3. **Importação Automatizada via Shapefile (`/mapas/upload/`)**:
   - Área administrativa restrita para importação de shapefiles compactados em arquivos `.zip`.
   - **Arrastar e Soltar (Drag & Drop)**: Interface interativa para carregar arquivos arrastando-os diretamente sobre a tela, com animação e destaque de borda ativa.
   - **Cruzamento Espacial Automático**: O backend intercepta os pontos importados e realiza um cruzamento geográfico off-line contra a malha municipal do RN para identificar e persistir o nome do município correspondente.
   - **Mapeamento de Atributos**: Extração automática das colunas de Status (`STATUS`, `status_operacional`, `Situação`) e Fonte (`FONTE`, `fonte_dado`, `Fonte`) do Shapefile do QGIS para o banco PostgreSQL.

4. **Painel Django Admin**:
   - Gerenciamento completo de todos os registros geoespaciais.
   - Organização automática por Município e Parque Eólico, com ferramentas de busca avançada, filtros laterais rápidos e visualização espacial do ponto no mapa administrativo.

---

## 📈 Status do Projeto

* **Fase de Modelagem & Banco de Dados:** Concluído (PostGIS/PostgreSQL integrado via Docker).
* **Fase de Desenvolvimento do WebGIS:** Concluído (Interface Leaflet, painéis estatísticos e marcadores dinâmicos).
* **Fase de Importação e SIG:** Concluído (Drag-and-drop de Shapefile + Cruzamento espacial de municípios).
* **Fase de Publicação de Dados:** Em Andamento.

---

## 💻 Tecnologias Utilizadas

- **Backend**: Django 4.2 & GeoDjango
- **Banco de Dados**: PostgreSQL & PostGIS (Dockerizado)
- **Frontend**: Vanilla HTML5, CSS3, Javascript, Leaflet & Leaflet.markercluster
- **Bibliotecas Espaciais**: GDAL/OGR, PROJ, GEOS & Turf.js

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- Docker e Docker Compose instalados na máquina.

### Execução passo a passo
1. Navegue até a pasta do banco de dados e inicialize os containers do Docker:
   ```bash
   cd PostGIS
   docker compose up -d
   ```
   *Isso irá construir a imagem do GeoDjango (`serido_django`) e inicializar o banco PostGIS (`serido_geodb`).*

2. A plataforma estará acessível em:
   - **Portal WebGIS:** `http://localhost:8000/` (redireciona automaticamente para `/mapas/`)
   - **Painel Admin:** `http://localhost:8000/admin/`

---

## 💾 Como realizar o Backup do Banco de Dados

Para realizar o backup do banco de dados espacial localizado no Docker de forma simples:

1. Navegue até a pasta do docker-compose:
   ```bash
   cd PostGIS
   ```

2. Execute o script de backup (usando Git Bash, WSL ou Linux):
   ```bash
   ./backup_db.sh
   ```

Os backups serão salvos no formato compactado do PostgreSQL (`.dump`) dentro do diretório `PostGIS/backups/`.

---

## 🌐 API de Dados Espaciais (WebGIS -> QGIS)

O projeto possui um endpoint (ponto de acesso) que extrai os dados vivos do banco de dados PostGIS e os converte automaticamente para o formato **GeoJSON**. Isso permite que softwares de SIG desktop (como o QGIS) consumam a base geométrica em tempo real via internet, sem necessidade de conexões diretas ao banco de dados.

### 📌 Endpoint Principal
* **URL Local:** `http://localhost:8000/mapas/api/eolicas/`
* **Método HTTP:** `GET`
* **Formato de Saída:** `application/json` (GeoJSON nativo)

### 🗺️ Como Consumir a API no QGIS (Passo a Passo)

Para carregar a camada vetorial das torres eólicas diretamente no QGIS utilizando este link, siga as instruções abaixo:

1. Abra o **QGIS**.
2. No menu superior, navegue em: **Camada** -> **Adicionar Camada** -> **Adicionar Camada Vetorial...** (ou use o atalho `Ctrl + Shift + V`).
3. Na janela que se abrir, mude a opção **Tipo de fonte** de *Arquivo* para **Protocolo: HTTP(S), cloud, etc.**
4. No campo **URI**, cole o link da API:
   ```text
   http://localhost:8000/mapas/api/eolicas/
   ```
5. Clique em **Adicionar**. A camada de pontos do banco PostGIS será carregada dinamicamente no seu projeto do QGIS.

---

## 🧑‍💻 Equipe

* **Pesquisadores (Bolsistas):** Maria Luiza e Igor Henrique
* **Orientador:** Flánelson Monteiro
* **Grupo de Pesquisa:** Processamento Mineral
* **Instituição:** Instituto Federal de Educação, Ciência e Tecnologia do Rio Grande do Norte (IFRN)
