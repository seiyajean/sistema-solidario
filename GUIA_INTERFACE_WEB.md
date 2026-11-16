# Interface web — Sistema Solidário

## Publicação

Use a branch `feat/interface-web-mvp`. Envie os arquivos deste pacote mantendo os caminhos relativos, sem apagar os demais arquivos do repositório.

## Execução local

1. Instale Python 3.12 e crie um ambiente virtual.
2. Execute `python -m pip install -r requirements.txt`.
3. Defina uma `SECRET_KEY` forte em variável de ambiente antes de usar dados reais.
4. Execute `flask --app run.py init-db`.
5. Execute `flask --app run.py criar-gestor` e informe nome, e-mail e senha.
6. Execute `python run.py` e abra `http://127.0.0.1:5000`.
7. Faça login e cadastre um alimento, registre uma doação e uma distribuição.
8. Execute `python -m pytest -q` e confira o workflow no GitHub Actions.

**Não use dados pessoais reais nas evidências acadêmicas.**

## Limites desta versão

O cadastro de gestor é feito via CLI, não há recuperação de senha ou gestão completa de contas. A interface tem validações e proteção CSRF, mas deve ser executada apenas em ambiente local/de demonstração até revisão adicional de segurança e implantação. O histórico mostra os últimos 50 registros de cada tipo.
