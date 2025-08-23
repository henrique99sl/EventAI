# Rollback - Reversão de Deploy

## Como reverter uma versão de produção

1. Localize o commit/tag anterior no Git:
   ```sh
   git checkout <tag-ou-commit-anterior>
   ```
2. Refaça o build da imagem Docker e faça o deploy.
3. Verifique os logs e o healthcheck.

## Como reverter banco de dados (se necessário)

1. Restaure o backup mais recente antes do deploy.
2. Siga os passos do RESTORE.md.