# Sistema Solidário

**Sistema web para gestão de doações, estoque e distribuição de alimentos em organizações comunitárias.**

> **Status:** em desenvolvimento — Experiência Prática III de Projeto de Software.

## Sobre o projeto

O **Sistema Solidário** é um projeto acadêmico de software concebido para apoiar organizações comunitárias no registro de doações de alimentos, acompanhamento do estoque e controle das distribuições. A proposta surgiu da identificação de dificuldades associadas a registros descentralizados e à rastreabilidade das movimentações.

O projeto toma como referência o contexto da **Associação Edificar**, em Novo Gama (GO), e busca oferecer uma solução simples para gestores e voluntários, considerando diferentes níveis de familiaridade com ferramentas digitais.

## Objetivo

Desenvolver um produto mínimo viável (MVP) que centralize as principais operações de recebimento, consulta e distribuição de alimentos, com regras de integridade do estoque e uma interface acessível.

O projeto se relaciona ao **Objetivo de Desenvolvimento Sustentável 2 (ODS 2 — Fome Zero e Agricultura Sustentável)**, especialmente à meta 2.1, por apoiar indiretamente a organização de iniciativas locais de assistência alimentar.

## Escopo do MVP

| Código | Funcionalidade | Prioridade |
| --- | --- | --- |
| RF01 | Autenticação de usuários | Obrigatória |
| RF02 | Cadastro de produtos | Obrigatória |
| RF03 | Registro de doações e entrada no estoque | Obrigatória |
| RF04 | Consulta ao estoque disponível | Obrigatória |
| RF05 | Registro de distribuições com verificação de saldo | Obrigatória |
| RF06 | Consulta ao histórico de movimentações | Obrigatória |
| RF07 | Relatórios consolidados por período | Evolução opcional |

### Regras de negócio principais

- As quantidades de doações e distribuições devem ser maiores que zero.
- Uma distribuição não pode exceder a quantidade disponível no estoque.
- Movimentações e atualizações de estoque devem ocorrer de forma consistente, em transações de banco de dados.
- Cada movimentação deve estar associada ao produto e ao usuário responsável.
- O MVP evita coletar dados pessoais desnecessários de doadores e beneficiários.

## Arquitetura e tecnologias planejadas

A aplicação adota uma **arquitetura monolítica em três camadas lógicas**:

1. **Apresentação:** HTML5, CSS3 e JavaScript, com interface responsiva.
2. **Aplicação:** Python 3.12 e Flask 3.1.x, responsáveis pelas rotas, validações e regras de negócio.
3. **Persistência:** SQLite e Flask-SQLAlchemy para armazenamento e movimentação dos dados.

Ferramentas e bibliotecas previstas:

- **Flask-WTF:** formulários e proteção CSRF.
- **Flask-Login e Werkzeug:** sessões de autenticação e armazenamento seguro de senhas por hash.
- **Pytest:** testes automatizados unitários e de integração.
- **Git e GitHub:** controle de versão e revisão por Pull Requests.
- **GitHub Actions:** integração contínua para execução automatizada de verificações e testes.

## Segurança, desempenho e acessibilidade

Os requisitos não funcionais orientam a implementação e a validação do MVP:

- Autenticação e autorização de acesso às operações do sistema.
- Validação de dados no servidor, proteção CSRF e cuidados contra vulnerabilidades comuns de aplicações web.
- Atualização consistente do estoque e mensagens claras para entradas inválidas.
- Interface responsiva, navegação por teclado, foco visível, contraste adequado e mensagens que não dependam exclusivamente de cores.
- Avaliação de desempenho em condições representativas de uso em dispositivos móveis.

## Prototipação e validação

Na Experiência Prática II foram elaboradas três representações de interface:

1. **Menu inicial:** acesso às principais funcionalidades.
2. **Registro de distribuição:** seleção do produto, quantidade e indicação de saldo.
3. **Resultado da distribuição:** exemplos de confirmação e alerta de estoque insuficiente.

Na Experiência Prática III, o desenvolvimento será acompanhado por testes automatizados, revisão de código e **duas rodadas de validação com representante externo da comunidade**, com registro de feedbacks e ajustes efetivamente realizados.

## Organização do desenvolvimento

O trabalho será registrado em commits semânticos, como:

- `docs:` documentação;
- `chore:` configuração e manutenção;
- `feat:` novas funcionalidades;
- `fix:` correções;
- `test:` testes automatizados.

Alterações relevantes serão propostas em branches e revisadas por meio de **Pull Requests** antes da integração à branch principal.

## Como executar

As instruções de instalação, configuração e execução serão incluídas conforme a estrutura executável do Flask for adicionada ao repositório. Até lá, este README documenta o escopo e as decisões técnicas do MVP.

## Contexto acadêmico

Projeto desenvolvido na disciplina **Projeto de Software**, em continuidade às Experiências Práticas I (diagnóstico e definição do MVP) e II (arquitetura, requisitos, prototipação e planejamento da validação).

**Repositório:** https://github.com/seiyajean/sistema-solidario
