"""Testes de integridade dos modelos com SQLite isolado."""

import pytest
from sqlalchemy.exc import IntegrityError

from app import create_app, db
from app.models import Produto, Usuario


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_usuario_senha_armazenada_com_hash(app):
    with app.app_context():
        usuario = Usuario(nome="Voluntária", email="voluntaria@example.org", perfil="voluntario")
        usuario.definir_senha("senha-de-teste-123")
        db.session.add(usuario)
        db.session.commit()
        assert usuario.senha_hash != "senha-de-teste-123"
        assert usuario.verificar_senha("senha-de-teste-123")
        assert not usuario.verificar_senha("senha-incorreta")


def test_email_de_usuario_deve_ser_unico(app):
    with app.app_context():
        for nome in ("Pessoa A", "Pessoa B"):
            usuario = Usuario(nome=nome, email="mesmo@example.org", perfil="gestor")
            usuario.definir_senha("senha-de-teste")
            db.session.add(usuario)
            if nome == "Pessoa A":
                db.session.commit()
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()


def test_perfil_de_usuario_deve_ser_valido(app):
    with app.app_context():
        usuario = Usuario(nome="Pessoa", email="pessoa@example.org", perfil="administrador")
        usuario.definir_senha("senha-de-teste")
        db.session.add(usuario)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()


def test_produto_estoque_inicial_zero(app):
    with app.app_context():
        produto = Produto(nome="Arroz", categoria="Cereais", unidade_medida="pacote")
        db.session.add(produto)
        db.session.commit()
        assert produto.quantidade_estoque == 0
        assert produto.ativo is True


def test_produto_nao_aceita_estoque_negativo(app):
    with app.app_context():
        produto = Produto(nome="Feijão", categoria="Grãos", unidade_medida="pacote", quantidade_estoque=-1)
        db.session.add(produto)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()
