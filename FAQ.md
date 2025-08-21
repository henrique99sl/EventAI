# FAQ / Troubleshooting

## Não consigo ligar à base de dados, erro "connection refused"
- Garante que o serviço da base de dados está a correr e as variáveis de ambiente estão corretas.
- Se usares Docker, usa o nome do serviço como host (`db`).

## Erro "Token inválido ou ausente"
- Garante que estás a enviar o header `Authorization: Bearer <token>` corretamente.
- O token pode ter expirado; faz login novamente.

## Como criar o primeiro admin?
- Podes criar manualmente na base de dados, ou alterar temporariamente o endpoint para aceitar role "admin".
- (Opcional: cria um script/endpoint protegido para este efeito)

## Migrations não aplicam mudanças
- Verifica se o diretório de migrations existe e está atualizado.
- Usa `flask db migrate` e `flask db upgrade`.

## Como popular a base de dados com dados de teste?
- Vê a secção de seed em MIGRATIONS.md.