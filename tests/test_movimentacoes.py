"""Testes de integração de entradas e saídas com SQLite isolado.

Execute com: python -m pytest -v
"""

import pytest
from sqlalchemy import func, select

from app import create_app, db
from app.distribuicoes import registrar_distribuicao
from app.doacoes import registrar_doacao
from app.models import Distribuicao, Doacao, Produto, Usuario


@pytest.fixture
def cenario():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "somente-testes",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        usuario = Usuario(nome="Voluntária Teste", email="voluntaria@example.org", perfil="voluntario")
        usuario.definir_senha("senha-exclusiva-de-teste")
        arroz = Produto(nome="Arroz", categoria="Cereais", unidade_medida="pacote", quantidade_estoque=20)
        feijao = Produto(nome="Feijão", categoria="Grãos", unidade_medida="pacote", quantidade_estoque=8)
        db.session.add_all([usuario, arroz, feijao])
        db.session.commit()
        yield usuario.id, arroz.id, feijao.id
        db.session.remove()
        db.drop_all()


def saldo(produto_id):
    return db.session.get(Produto, produto_id).quantidade_estoque


def contagem(modelo):
    return db.session.scalar(select(func.count()).select_from(modelo))


def test_fluxo_completo_entrada_e_saida_preserva_saldo(cenario):
    usuario_id, arroz_id, _ = cenario
    registrar_doacao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=10)
    registrar_distribuicao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=7)
    assert saldo(arroz_id) == 23
    assert contagem(Doacao) == 1
    assert contagem(Distribuicao) == 1


def test_operacoes_sucessivas_registram_todas_as_movimentacoes(cenario):
    usuario_id, arroz_id, _ = cenario
    for quantidade in (2, 3, 5):
        registrar_doacao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=quantidade)
    for quantidade in (4, 6):
        registrar_distribuicao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=quantidade)
    assert saldo(arroz_id) == 20
    assert contagem(Doacao) == 3
    assert contagem(Distribuicao) == 2


def test_estoque_insuficiente_apos_doacao_nao_cria_saida(cenario):
    usuario_id, arroz_id, _ = cenario
    registrar_doacao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=5)
    with pytest.raises(ValueError, match="Estoque insuficiente"):
        registrar_distribuicao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=26)
    assert saldo(arroz_id) == 25
    assert contagem(Doacao) == 1
    assert contagem(Distribuicao) == 0


def test_movimentacoes_de_um_produto_nao_alteram_outro(cenario):
    usuario_id, arroz_id, feijao_id = cenario
    registrar_doacao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=4)
    registrar_distribuicao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=6)
    assert saldo(arroz_id) == 18
    assert saldo(feijao_id) == 8


def test_erro_de_distribuicao_nao_impede_doacao_posterior(cenario):
    usuario_id, arroz_id, _ = cenario
    with pytest.raises(ValueError, match="Estoque insuficiente"):
        registrar_distribuicao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=21)
    registrar_doacao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=2)
    assert saldo(arroz_id) == 22
    assert contagem(Distribuicao) == 0
    assert contagem(Doacao) == 1


def test_distribuicao_exata_apos_entrada_termina_em_zero(cenario):
    usuario_id, arroz_id, _ = cenario
    registrar_doacao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=5)
    registrar_distribuicao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=25)
    assert saldo(arroz_id) == 0
    assert contagem(Doacao) == 1
    assert contagem(Distribuicao) == 1


def test_entrada_invalida_nao_afeta_distribuicao_valida(cenario):
    usuario_id, arroz_id, _ = cenario
    with pytest.raises(ValueError):
        registrar_doacao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=0)
    registrar_distribuicao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=5)
    assert saldo(arroz_id) == 15
    assert contagem(Doacao) == 0
    assert contagem(Distribuicao) == 1


def test_movimentacoes_preservam_referencia_ao_usuario_e_produto(cenario):
    usuario_id, arroz_id, _ = cenario
    doacao = registrar_doacao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=3)
    distribuicao = registrar_distribuicao(produto_id=arroz_id, usuario_id=usuario_id, quantidade=2)
    assert (doacao.produto_id, doacao.registrado_por) == (arroz_id, usuario_id)
    assert (distribuicao.produto_id, distribuicao.registrado_por) == (arroz_id, usuario_id)
