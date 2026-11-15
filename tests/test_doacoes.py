"""Testes de integração da regra de entrada de alimentos (SQLite em memória)."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import create_app, db
from app.doacoes import registrar_doacao
from app.models import Doacao, Produto, Usuario


@pytest.fixture
def base():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        usuario = Usuario(nome="Voluntária", email="teste@example.org", perfil="voluntario")
        usuario.definir_senha("senha-de-teste")
        produto = Produto(nome="Arroz", categoria="Cereais", unidade_medida="pacote", quantidade_estoque=20)
        db.session.add_all([usuario, produto])
        db.session.commit()
        yield usuario.id, produto.id
        db.session.remove()
        db.drop_all()


def test_doacao_aumenta_estoque_e_registra_historico(base):
    usuario_id, produto_id = base
    doacao = registrar_doacao(produto_id=produto_id, usuario_id=usuario_id, quantidade=5)
    assert doacao.id is not None
    assert doacao.data is not None
    assert db.session.get(Produto, produto_id).quantidade_estoque == 25
    assert db.session.scalar(select(Doacao).where(Doacao.id == doacao.id)).quantidade == 5


@pytest.mark.parametrize("quantidade", [0, -1, 2.5, True, "3"])
def test_quantidade_invalida_nao_altera_estoque(base, quantidade):
    usuario_id, produto_id = base
    with pytest.raises(ValueError):
        registrar_doacao(produto_id=produto_id, usuario_id=usuario_id, quantidade=quantidade)
    assert db.session.get(Produto, produto_id).quantidade_estoque == 20
    assert db.session.scalar(select(Doacao.id)) is None


def test_produto_inexistente_nao_cria_doacao(base):
    usuario_id, produto_id = base
    with pytest.raises(ValueError, match="Produto"):
        registrar_doacao(produto_id=999, usuario_id=usuario_id, quantidade=5)
    assert db.session.get(Produto, produto_id).quantidade_estoque == 20
    assert db.session.scalar(select(Doacao.id)) is None


def test_usuario_inativo_nao_registra_doacao(base):
    usuario_id, produto_id = base
    usuario = db.session.get(Usuario, usuario_id)
    usuario.ativo = False
    db.session.commit()
    with pytest.raises(ValueError, match="Usuário"):
        registrar_doacao(produto_id=produto_id, usuario_id=usuario_id, quantidade=5)
    assert db.session.get(Produto, produto_id).quantidade_estoque == 20


def test_produto_inativo_nao_registra_doacao(base):
    usuario_id, produto_id = base
    produto = db.session.get(Produto, produto_id)
    produto.ativo = False
    db.session.commit()
    with pytest.raises(ValueError, match="Produto"):
        registrar_doacao(produto_id=produto_id, usuario_id=usuario_id, quantidade=5)
    assert db.session.get(Produto, produto_id).quantidade_estoque == 20


def test_restricao_do_banco_rejeita_quantidade_negativa(base):
    usuario_id, produto_id = base
    db.session.add(Doacao(produto_id=produto_id, registrado_por=usuario_id, quantidade=-3, data=__import__('datetime').datetime.now()))
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()
