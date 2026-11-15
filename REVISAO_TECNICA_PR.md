# Auto-revisão técnica — validação de movimentações

## Contexto
As funções `registrar_doacao` e `registrar_distribuicao` repetiam as mesmas verificações de quantidade, identificadores e usuário ativo. Isso poderia levar a regras divergentes durante futuras alterações.

## Alterações
- Centralização das verificações em `app/validacoes.py`.
- Rejeição explícita de IDs não positivos, booleanos e valores não inteiros antes de abrir a transação.
- Substituição dos blocos duplicados em `app/doacoes.py` e `app/distribuicoes.py`.
- Preservação do `UPDATE` condicional para estoque e do `commit`/`rollback` transacional.
- Inclusão de testes unitários parametrizados para entradas válidas e inválidas.

## Checklist de auto-revisão
- [x] **Arquitetura:** validações de domínio isoladas das operações de persistência.
- [x] **Legibilidade:** mensagens de erro explícitas e funções pequenas.
- [x] **Segurança:** rejeição de booleanos, identificadores não positivos e quantidades inválidas.
- [x] **Integridade:** atualização atômica e reversão transacional preservadas.
- [ ] **Testes completos:** executar `python -m pytest -q` em ambiente com as dependências instaladas e registrar o resultado real.
- [ ] **Revisão do diff:** conferir os arquivos em *Files changed* antes do merge.

## Limitações
A validação de usuário ativo por ID não substitui autenticação/autorização HTTP. Essa integração será necessária antes de expor endpoints de movimentação ao público.
