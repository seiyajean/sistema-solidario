"""Regra de negócio para recebimento de alimentos.

A operação é usada inicialmente por um comando administrativo local. A exposição
via HTTP dependerá da implementação de autenticação e autorização (RF01).
"""

from datetime import datetime, timezone

from sqlalchemy import update

from app import db
from app.validacoes import validar_parametros_movimentacao, validar_usuario_ativo
from app.models import Doacao, Produto, Usuario


def registrar_doacao(*, produto_id: int, usuario_id: int, quantidade: int) -> Doacao:
    """Registra entrada e aumenta o saldo na mesma transação.

    Em caso de falha, a sessão é revertida, sem deixar movimentação parcial.
    """
    validar_parametros_movimentacao(
        produto_id=produto_id, usuario_id=usuario_id, quantidade=quantidade
    )

    try:
        usuario = db.session.get(Usuario, usuario_id)
        validar_usuario_ativo(usuario)

        # UPDATE atômico impede perda de incrementos em requisições concorrentes.
        resultado = db.session.execute(
            update(Produto)
            .where(Produto.id == produto_id, Produto.ativo.is_(True))
            .values(quantidade_estoque=Produto.quantidade_estoque + quantidade)
        )
        if resultado.rowcount != 1:
            raise ValueError("Produto inexistente ou inativo.")

        doacao = Doacao(
            produto_id=produto_id,
            registrado_por=usuario_id,
            quantidade=quantidade,
            data=datetime.now(timezone.utc),
        )
        db.session.add(doacao)
        db.session.commit()
        return doacao
    except Exception:
        db.session.rollback()
        raise
