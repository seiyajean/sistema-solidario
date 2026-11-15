"""Registro transacional de saídas de estoque (uso administrativo local)."""
from datetime import datetime, timezone
from sqlalchemy import update
from app import db
from app.validacoes import validar_parametros_movimentacao, validar_usuario_ativo
from app.models import Distribuicao, Produto, Usuario


def registrar_distribuicao(*, produto_id: int, usuario_id: int, quantidade: int) -> Distribuicao:
    """Deduz estoque apenas se houver saldo suficiente e registra a saída.

    O UPDATE condicional evita estoque negativo inclusive em operações concorrentes.
    A gravação da distribuição e a dedução do estoque ocorrem na mesma transação.
    """
    validar_parametros_movimentacao(
        produto_id=produto_id, usuario_id=usuario_id, quantidade=quantidade
    )

    try:
        usuario = db.session.get(Usuario, usuario_id)
        validar_usuario_ativo(usuario)

        resultado = db.session.execute(
            update(Produto)
            .where(
                Produto.id == produto_id,
                Produto.ativo.is_(True),
                Produto.quantidade_estoque >= quantidade,
            )
            .values(quantidade_estoque=Produto.quantidade_estoque - quantidade)
        )
        if resultado.rowcount != 1:
            produto = db.session.get(Produto, produto_id)
            if produto is None or not produto.ativo:
                raise ValueError("Produto inexistente ou inativo.")
            raise ValueError("Estoque insuficiente para a distribuição solicitada.")

        distribuicao = Distribuicao(
            produto_id=produto_id, registrado_por=usuario_id,
            quantidade=quantidade, data=datetime.now(timezone.utc),
        )
        db.session.add(distribuicao)
        db.session.commit()
        return distribuicao
    except Exception:
        db.session.rollback()
        raise
