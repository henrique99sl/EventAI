# Guia de Deploy/Produção

Este guia explica como preparar e lançar o EventAI Backend num ambiente de produção.

## Pré-requisitos

- Docker e Docker Compose
- Variáveis de ambiente seguras (.env)
- Base de dados PostgreSQL configurada

## Passos

1. **Configura as variáveis de ambiente**
   - Usa um ficheiro `.env` com:
     ```
     DATABASE_URL=postgresql://user:password@host:5432/dbname
     SECRET_KEY=uma_chave_ultra_secreta
     ```
2. **Constrói as imagens Docker**
   ```bash
   docker-compose build
   ```
3. **Sobe os containers**
   ```bash
   docker-compose up -d
   ```
4. **Aplica as migrations**
   ```bash
   docker-compose exec backend flask db upgrade
   ```
5. **(Opcional) Configura HTTPS e um reverse proxy (nginx, traefik, etc.)**
   - Não exposes o Flask diretamente para a internet em produção.

## Boas práticas

- Mantém `DEBUG=False` em produção.
- Usa uma `SECRET_KEY` longa e secreta.
- Limita permissões da DB.
- Usa logs centralizados.
- Faz backups regulares.

## Troubleshooting

- Verifica logs com `docker-compose logs`.
- Consulta o FAQ para problemas comuns.