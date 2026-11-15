"""Testes unitários das validações compartilhadas, sem acesso ao banco."""

import pytest

from app.validacoes import validar_parametros_movimentacao, validar_usuario_ativo


@pytest.mark.parametrize("quantidade", [0, -1, True, False, 1.5, "5", None])
def test_rejeita_quantidade_invalida(quantidade):
    with pytest.raises(ValueError, match="quantidade"):
        validar_parametros_movimentacao(produto_id=1, usuario_id=1, quantidade=quantidade)


@pytest.mark.parametrize("identificador", [0, -1, True, False, 2.5, "1", None])
def test_rejeita_identificador_invalido(identificador):
    with pytest.raises(ValueError, match="identificadores"):
        validar_parametros_movimentacao(produto_id=identificador, usuario_id=1, quantidade=5)
    with pytest.raises(ValueError, match="identificadores"):
        validar_parametros_movimentacao(produto_id=1, usuario_id=identificador, quantidade=5)


def test_aceita_parametros_validos():
    assert validar_parametros_movimentacao(produto_id=1, usuario_id=2, quantidade=5) is None


@pytest.mark.parametrize("usuario", [None, type("U", (), {"ativo": False})()])
def test_rejeita_usuario_inexistente_ou_inativo(usuario):
    with pytest.raises(ValueError, match="inexistente ou inativo"):
        validar_usuario_ativo(usuario)


def test_aceita_usuario_ativo():
    assert validar_usuario_ativo(type("U", (), {"ativo": True})()) is None
