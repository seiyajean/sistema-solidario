# Sétimo commit — Testes de movimentações

## Objetivo

Ampliar os testes de integração do Sistema Solidário para verificar doações e distribuições sucessivas, saldo correto, isolamento entre produtos, histórico e comportamento após erros.

## Arquivo novo

- `tests/test_movimentacoes.py` — oito cenários de integração, usando SQLite em memória e dados fictícios.

**Importante:** este pacote acrescenta testes; não modifica as regras de negócio. Os testes ainda precisam ser executados em ambiente com as dependências instaladas.

## Publicação pelo site do GitHub

1. Extraia o ZIP.
2. Abra https://github.com/seiyajean/sistema-solidario.
3. Clique em **Add file → Upload files**.
4. Envie `tests/test_movimentacoes.py` preservando a pasta `tests/` e `GUIA_COMMIT_07.md` na raiz.
5. Em **Commit message**, digite: `test: ampliar testes automatizados de movimentações`.
6. Em **Extended description** (opcional), digite: `Adiciona oito cenários de integração para entradas, saídas, saldo, histórico e recuperação após erros.`
7. Confirme o commit e confira o título no histórico.

## Executar os testes (Windows / PowerShell)

Baixe o repositório completo pelo botão **Code → Download ZIP** e extraia em uma pasta local. Abra um terminal nessa pasta.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
```

Se o comando `py -3.12` não funcionar, verifique a instalação do Python 3.12 e use `python -m venv .venv` se a versão correta estiver configurada.

**Evidência acadêmica:** capture a saída completa do Pytest com o número de testes executados e o resultado, sem afirmar aprovação antes da execução.

## Observações

- A cobertura não foi medida neste commit; será tratada na etapa de testes e integração contínua.
- O repositório público deve conter apenas dados fictícios, nunca banco de dados real, senhas ou segredos.
- O pacote não implementa interface web de cadastro, login ou autenticação; essas entregas continuam pendentes.
