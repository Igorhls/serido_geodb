# BDG Seridó Renovável

Repositório oficial do projeto de pesquisa: **Estudo da construção de um banco de dados geoespacial de energia renovável: vetorização e mapeamento aplicado na Região do Seridó Potiguar.**

Projeto vinculado ao Edital nº 19/2025 - PROPI/RE/IFRN - PIBIC-Af/CNPq.

---

## 🎯 Objetivo

Este projeto visa construir um banco de dados geoespacial vetorial sobre os empreendimentos de energia eólica e solar na Região do Seridó Potiguar (RN).

O objetivo é organizar e disponibilizar gratuitamente dados atualizados e padronizados para pesquisadores, gestores públicos e a comunidade acadêmica, facilitando o planejamento energético e ambiental na região.

## 📈 Status do Projeto

* **Fase Atual:** Em Andamento (Fase de Planejamento e Estruturação do Banco de Dados).

## 🧑‍💻 Equipe

* **Pesquisadores (Bolsistas):** Maria Luiza e Igor Henrique
* **Orientador:** Flánelson Monteiro
*  **Grupo de Pesquisa:** Processamento Mineral
* **Instituição:** Instituto Federal de Educação, Ciência e Tecnologia do Rio Grande do Norte (IFRN)

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

## 🌐 API de Dados Espaciais (WebGIS -> QGIS)

O projeto possui um endpoint (ponto de acesso) que extrai os dados vivos do banco de dados PostGIS e os converte automaticamente para o formato **GeoJSON**. Isso permite que softwares de SIG desktop (como o QGIS) consumam a base geométrica em tempo real via internet, sem necessidade de conexões diretas ao banco de dados.

### 📌 Endpoint Principal
* **URL Local:** `http://localhost:8000/mapas/api/eolicas/`
* **Método HTTP:** `GET`
* **Formato de Saída:** `application/json` (GeoJSON nativo)

---

### 🗺️ Como Consumir a API no QGIS (Passo a Passo)

Para carregar a camada vetorial das torres eólicas diretamente no QGIS utilizando este link, siga as instruções abaixo:

1. Abra o **QGIS**.
2. No menu superior, navegue em: **Camada** -> **Adicionar Camada** -> **Adicionar Camada Vetorial...** (ou use o atalho `Ctrl + Shift + V`).
3. Na janela que se abrir, mude a opção **Tipo de fonte** de *Arquivo* para **Protocolo: HTTP(S), cloud, etc.**
4. No campo **URI**, cole o link da API:
   ```text
   http://localhost:8000/mapas/api/eolicas/

