# Terceiro commit — Estrutura Flask

Esta pasta contém os **arquivos novos** para adicionar ao repositório existente. Preserve o README.md e o .gitignore que já estão no GitHub.

## Publicação recomendada (Git local)

1. Clone seu repositório público: `git clone https://github.com/seiyajean/sistema-solidario.git`
2. Copie o conteúdo desta pasta para dentro da pasta clonada (sem apagar arquivos existentes).
3. Confira que o `.gitignore` ignora `.env`, `instance/`, `__pycache__/`, `.pytest_cache/` e `.venv/`.
4. Execute os comandos:

```bash
cd sistema-solidario
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python run.py
```

5. Abra `http://127.0.0.1:5000/` e confira a página inicial. Encerre o servidor com Ctrl+C.
6. Registre o commit:

```bash
git add app run.py requirements.txt .env.example tests
# opcional: git add INSTRUCOES.md
git commit -m "chore: configurar estrutura Flask e dependências"
git push origin main
```

Se preferir subir os arquivos pelo site do GitHub, use **Add file → Upload files**, arraste os arquivos e pastas (sem a pasta raiz `sistema-solidario`) e digite a mensagem do commit acima.

**Atenção:** `SECRET_KEY` padrão é somente para desenvolvimento local. Antes de publicar ou disponibilizar a aplicação em produção, defina uma chave secreta segura em variável de ambiente e habilite HTTPS, controles de sessão e demais proteções planejadas. O arquivo `.env.example` é apenas um modelo, não é lido automaticamente.
