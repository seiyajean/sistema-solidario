"""Testes de integração da distribuição com SQLite em memória."""
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.distribuicoes import registrar_distribuicao
from app.models import Distribuicao, Produto, Usuario

@pytest.fixture
def base():
    app = create_app({"TESTING": True, "SECRET_KEY": "test-only",
                      "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        usuario = Usuario(nome="Voluntária", email="voluntaria@example.org", perfil="voluntario")
        usuario.definir_senha("senha-de-teste")
        produto = Produto(nome="Arroz", categoria="Cereais", unidade_medida="pacote", quantidade_estoque=20)
        db.session.add_all([usuario, produto])
        db.session.commit()
        yield usuario.id, produto.id
        db.session.remove()
        db.drop_all()

def test_distribuicao_reduz_estoque_e_grava_historico(base):
    uid, pid = base
    registro = registrar_distribuicao(produto_id=pid, usuario_id=uid, quantidade=5)
    assert registro.id is not None
    assert registro.data is not None
    assert db.session.get(Produto, pid).quantidade_estoque == 15
    assert db.session.scalar(select(Distribuicao).where(Distribuicao.id == registro.id)).quantidade == 5

def test_distribuicao_exata_zerar_estoque(base):
    uid, pid = base
    registrar_distribuicao(produto_id=pid, usuario_id=uid, quantidade=20)
    assert db.session.get(Produto, pid).quantidade_estoque == 0

def test_estoque_insuficiente_preserva_saldo_e_historico(base):
    uid, pid = base
    with pytest.raises(ValueError, match="Estoque insuficiente"):
        registrar_distribuicao(produto_id=pid, usuario_id=uid, quantidade=25)
    assert db.session.get(Produto, pid).quantidade_estoque == 20
    assert db.session.scalar(select(Distribuicao.id)) is None

@pytest.mark.parametrize("quantidade", [0, -1, 2.5, True, "3"])
def test_quantidades_invalidas_nao_alteram_saldo(base, quantidade):
    uid, pid = base
    with pytest.raises(ValueError):
        registrar_distribuicao(produto_id=pid, usuario_id=uid, quantidade=quantidade)
    assert db.session.get(Produto, pid).quantidade_estoque == 20
    assert db.session.scalar(select(Distribuicao.id)) is None

def test_usuario_inativo_nao_distribui(base):
    uid, pid = base
    db.session.get(Usuario, uid).ativo = False
    db.session.commit()
    with pytest.raises(ValueError, match="Usuário"):
        registrar_distribuicao(produto_id=pid, usuario_id=uid, quantidade=2)
    assert db.session.get(Produto, pid).quantidade_estoque == 20

def test_produto_inativo_nao_distribui(base):
    uid, pid = base
    db.session.get(Produto, pid).ativo = False
    db.session.commit()
    with pytest.raises(ValueError, match="Produto"):
        registrar_distribuicao(produto_id=pid, usuario_id=uid, quantidade=2)
    assert db.session.get(Produto, pid).quantidade_estoque == 20

def test_produto_inexistente_nao_distribui(base):
    uid, pid = base
    with pytest.raises(ValueError, match="Produto"):
        registrar_distribuicao(produto_id=999, usuario_id=uid, quantidade=2)
    assert db.session.get(Produto, pid).quantidade_estoque == 20

def test_usuario_inexistente_nao_distribui(base):
    _, pid = base
    with pytest.raises(ValueError, match="Usuário"):
        registrar_distribuicao(produto_id=pid, usuario_id=999, quantidade=2)
    assert db.session.get(Produto, pid).quantidade_estoque == 20

def test_restricao_sql_rejeita_quantidade_negativa(base):
    from datetime import datetime, timezone
    uid, pid = base
    db.session.add(Distribuicao(produto_id=pid, registrado_por=uid, quantidade=-1,
                                data=datetime.now(timezone.utc)))
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()
