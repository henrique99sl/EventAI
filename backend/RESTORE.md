# Restore - Recuperação de ambiente/projeto

## Como restaurar um backup do banco de dados

1. Localize o arquivo de backup (.sql ou .dump).
2. Execute o comando:
   ```sh
   psql -U <usuario> -d <dbname> < backup.sql
   ```
3. Verifique se o serviço está rodando normalmente.

## Como restaurar arquivos do projeto

1. Recupere o diretório desejado via backup/snapshot.
2. Restaure usando:
   ```sh
   rsync -av <origem> <destino>
   ```