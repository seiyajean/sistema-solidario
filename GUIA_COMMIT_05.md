# Quinto commit — Registro de doações

## Conteúdo do pacote

Atualize os arquivos `app/__init__.py` e `app/models.py`. Adicione `app/doacoes.py`, `tests/test_doacoes.py` e este guia. **Não substitua o repositório inteiro** nem apague arquivos anteriores.

## Publicação pelo navegador

1. Extraia o ZIP, mantendo as pastas `app` e `tests`.
2. Abra https://github.com/seiyajean/sistema-solidario na branch `main`.
3. Use **Add file → Upload files** e arraste os arquivos extraídos. O GitHub deve indicar a substituição dos dois arquivos existentes e a criação dos demais.
4. No campo **Commit message** (primeiro campo, não na descrição opcional), informe:
   `feat: implementar registro de doações e atualização do estoque`
5. Confirme o commit e confira o título no histórico.

## Testar no computador

Use Python 3.12 e, na pasta do projeto:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m flask --app run:app init-db
python -m pytest -q
```

Se `run.py` não exportar a variável `app`, consulte-o e adapte o comando Flask ao ponto de entrada existente. `init-db` cria tabelas ausentes; **não é um mecanismo de migração de esquemas existentes**.

### Registro de doação pela linha de comando

O comando abaixo exige que os IDs 1 de usuário e produto **já existam** no banco:

```powershell
python -m flask --app run:app registrar-doacao --produto 1 --usuario 1 --quantidade 5
```

Este commit implementa a entidade Doação, a regra transacional e um comando administrativo **local**. Ainda **não implementa** formulário web de doação nem login/autorização HTTP: expor uma rota de escrita sem autenticação seria inseguro. Essas interfaces devem ser integradas nos próximos commits.

## Evidências

Guarde captura do histórico de commits com a mensagem correta e, após executar localmente, capture a saída do Pytest. Não declare testes aprovados sem executá-los.
