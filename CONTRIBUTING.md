# Guia de Contribuição

Obrigado pelo interesse em contribuir para o EventAI!  
Todas as contribuições são bem-vindas: código, documentação, testes, sugestões e correção de bugs.

## Como contribuir

1. Fork este repositório e faz clone para o teu computador.
2. Cria uma branch para a tua feature/correção:
   ```bash
   git checkout -b minha-feature
   ```
3. Faz as tuas alterações.  
   Garante que o código segue a PEP8 e que os testes passam.
4. Adiciona/atualiza testes se aplicável.
5. Faz commit das alterações.
6. Sobe a branch:
   ```bash
   git push origin minha-feature
   ```
7. Abre um Pull Request para a branch `main` com uma descrição clara.

## Normas de código

- Usa nomes descritivos para funções e variáveis.
- Escreve docstrings nas funções/métodos principais.
- Garante cobertura de testes para novas funcionalidades.
- Segue as boas práticas da comunidade Flask/Python.

## Como testar localmente

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest
```

## Sugestão de issues

- Usa as labels "bug", "feature", "question" conforme apropriado.
- Inclui passos para reproduzir, comportamento esperado e real, prints/logs se possível.

Em caso de dúvida, abre uma issue ou contacta os maintainers!