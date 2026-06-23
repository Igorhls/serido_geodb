#!/bin/bash

# Script de Backup Automatizado para o Banco de Dados PostGIS
#
# Para executar manualmente:
#   1. Abra o terminal (Git Bash, WSL ou Linux).
#   2. Navegue até a pasta do docker-compose:
#      cd /c/Users/igorh/Documents/Code/serido_geodb/PostGIS
#   3. Execute o script:
#      ./backup_db.sh
#

# Define o diretório de destino
BACKUP_DIR="backups"

# Cria a pasta de backups caso não exista
mkdir -p "$BACKUP_DIR"

# Obtém a data e hora atual formatada
DATA=$(date +%Y-%m-%d_%H-%M-%S)

# Nome do arquivo de dump
FILE_NAME="$BACKUP_DIR/backup_serido_$DATA.dump"

echo "Iniciando o backup do banco de dados serido_renovavel..."

# Executa o dump dentro do contêiner e salva no arquivo local
docker-compose exec -T postgis pg_dump -U igorhls -d serido_renovavel -F c > "$FILE_NAME"

# Verifica se o comando foi executado com sucesso
if [ $? -eq 0 ]; then
    echo "Backup concluído com sucesso!"
    echo "Arquivo gerado: $FILE_NAME"
else
    echo "Erro ao realizar o backup!"
    rm -f "$FILE_NAME"
    exit 1
fi
