# Sexto commit — Distribuição de alimentos

Mensagem **no primeiro campo** do GitHub:

`feat: implementar distribuição com validação de estoque`

## Arquivos para enviar
- `app/models.py` (substituir o existente)
- `app/distribuicoes.py` (novo)
- `app/__init__.py` (substituir o existente)
- `tests/test_distribuicoes.py` (novo)
- `GUIA_COMMIT_06.md` (novo)

**Não envie o ZIP diretamente para o repositório**; extraia-o e mantenha os caminhos. Não apague os arquivos anteriores.

## Executar localmente

No terminal, na raiz do projeto, com Python 3.12:

```bash
python -m venv .venv
```

Ative o ambiente (Windows PowerShell: `.venv\Scripts\Activate.ps1`; CMD: `.venv\Scripts\activate.bat`). Depois:

```bash
python -m pip install -r requirements.txt
python -m flask --app run.py init-db
python -m pytest -q
```

Para registrar uma distribuição, é necessário que já existam um usuário e um produto ativos no banco, com saldo suficiente. Exemplo com IDs reais de seu banco:

```bash
python -m flask --app run.py registrar-distribuicao --produto 1 --usuario 1 --quantidade 5
```

O saldo é deduzido e a saída é gravada em uma única transação. Uma solicitação acima do saldo é rejeitada, sem modificar o estoque. A operação permanece restrita ao comando local, sem rota web pública, até que autenticação e autorização sejam implementadas.

## Publicar pelo GitHub web
1. Abra https://github.com/seiyajean/sistema-solidario.
2. Use **Add file > Upload files**.
3. Arraste os cinco arquivos mantendo as pastas `app/` e `tests/`; confirme a substituição dos dois arquivos existentes.
4. No campo **Commit message** (título), cole a mensagem semântica indicada acima.
5. No campo **Extended description** (opcional), descreva a validação de saldo e os testes.
6. Confirme o commit e confira o histórico.

**Evidências:** capture o histórico com SHA e título; depois, em ambiente com dependências instaladas, registre a saída real do pytest. Não apresente os testes como executados antes de verificá-los.
