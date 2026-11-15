"""Regra de negócio para recebimento de alimentos.

A operação é usada inicialmente por um comando administrativo local. A exposição
via HTTP dependerá da implementação de autenticação e autorização (RF01).
"""

from datetime import datetime, timezone

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import Doacao, Produto, Usuario


def registrar_doacao(*, produto_id: int, usuario_id: int, quantidade: int) -> Doacao:
    """Registra entrada e aumenta o saldo na mesma transação.

    Em caso de falha, a sessão é revertida, sem deixar movimentação parcial.
    """
    if type(quantidade) is not int or quantidade <= 0:
        raise ValueError("A quantidade deve ser um número inteiro positivo.")
    if type(produto_id) is not int or type(usuario_id) is not int:
        raise ValueError("Os identificadores devem ser números inteiros.")

    try:
        usuario = db.session.get(Usuario, usuario_id)
        if usuario is None or not usuario.ativo:
            raise ValueError("Usuário inexistente ou inativo.")

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
