# Checklist de Deploy em Produção

- [ ] Todos os testes passaram (`pytest`, `lint`, etc)
- [ ] Docker build executado sem erros
- [ ] Healthcheck OK (`/health` responde 200)
- [ ] Backup de banco de dados realizado
- [ ] Backup do diretório de arquivos realizado
- [ ] Migrações aplicadas (`flask db upgrade`)
- [ ] Variáveis de ambiente revisadas
- [ ] Rollback testado em ambiente de homologação
- [ ] Checklist revisado por outro desenvolvedor