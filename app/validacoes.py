"""Validações compartilhadas pelas movimentações de estoque."""


def validar_parametros_movimentacao(*, produto_id: int, usuario_id: int, quantidade: int) -> None:
    """Rejeita valores inválidos antes de iniciar a transação.

    ``type(...) is int`` evita aceitar booleanos como identificadores ou quantidades.
    """
    if type(quantidade) is not int or quantidade <= 0:
        raise ValueError("A quantidade deve ser um número inteiro positivo.")
    if (type(produto_id) is not int or produto_id <= 0
            or type(usuario_id) is not int or usuario_id <= 0):
        raise ValueError("Os identificadores devem ser números inteiros positivos.")


def validar_usuario_ativo(usuario: object) -> None:
    """Exige um usuário existente e ativo."""
    if usuario is None or not usuario.ativo:
        raise ValueError("Usuário inexistente ou inativo.")
