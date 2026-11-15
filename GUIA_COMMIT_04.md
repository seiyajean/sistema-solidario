# Quarto commit — Modelos de usuários e produtos

Este pacote contém **somente os arquivos novos ou alterados** em relação ao terceiro commit. Preserve os demais arquivos do repositório.

## Arquivos
- `app/models.py`: entidades `Usuario` e `Produto`, restrições e hash de senha.
- `app/__init__.py`: importa modelos e disponibiliza comando `init-db`.
- `tests/test_models.py`: cinco testes para regras de persistência.

## Instalação e execução local (PowerShell)

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
$env:FLASK_APP = "run.py"
python -m flask init-db
python run.py
```

Acesse http://127.0.0.1:5000/ e http://127.0.0.1:5000/health.

**Importante:** `init-db` cria as tabelas no banco configurado, mas não faz migrações de esquemas existentes. Não execute em banco de produção sem planejar migrações e backups. Os testes usam SQLite em memória e dados fictícios. O hash scrypt é custoso por design e pode tornar o teste de senha um pouco mais demorado.

## Commit recomendado

```bash
git add app/__init__.py app/models.py tests/test_models.py GUIA_COMMIT_04.md
git commit -m "feat: implementar modelos de usuários e produtos"
git push origin main
```

Se fizer upload pelo site, confira a estrutura das pastas e **digite a mensagem acima** no campo do commit, em vez de aceitar `Add files via upload`.
