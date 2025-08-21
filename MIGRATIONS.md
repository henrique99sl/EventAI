# Migrations & Seed

## Como criar uma migration

```bash
flask db migrate -m "Descrição da alteração"
```

## Como aplicar migrations

```bash
flask db upgrade
```

## Como reverter uma migration

```bash
flask db downgrade
```

## Como popular a base de dados (seed)

- Cria um script Python (ex: `seed.py`) com a lógica de inserção dos dados de teste.
- Corre o script no contexto do backend:
  ```bash
  docker-compose exec backend python seed.py
  ```

## Dica

- Mantém o diretório `migrations/` sob controlo de versão.
- Não edites migrations já aplicadas em produção!