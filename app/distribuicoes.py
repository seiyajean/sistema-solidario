"""Registro transacional de saídas de estoque (uso administrativo local)."""
from datetime import datetime, timezone
from sqlalchemy import update
from app import db
from app.models import Distribuicao, Produto, Usuario


def registrar_distribuicao(*, produto_id: int, usuario_id: int, quantidade: int) -> Distribuicao:
    """Deduz estoque apenas se houver saldo suficiente e registra a saída.

    O UPDATE condicional evita estoque negativo inclusive em operações concorrentes.
    A gravação da distribuição e a dedução do estoque ocorrem na mesma transação.
    """
    if type(quantidade) is not int or quantidade <= 0:
        raise ValueError("A quantidade deve ser um número inteiro positivo.")
    if type(produto_id) is not int or type(usuario_id) is not int:
        raise ValueError("Os identificadores devem ser números inteiros.")

    try:
        usuario = db.session.get(Usuario, usuario_id)
        if usuario is None or not usuario.ativo:
            raise ValueError("Usuário inexistente ou inativo.")

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
