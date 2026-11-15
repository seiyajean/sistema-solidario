"""Modelos de persistência do Sistema Solidário."""

from sqlalchemy import CheckConstraint, UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class Usuario(db.Model):
    """Pessoa autorizada a operar o sistema."""

    __tablename__ = "usuarios"
    __table_args__ = (
        UniqueConstraint("email", name="uq_usuarios_email"),
        CheckConstraint("perfil IN ('gestor', 'voluntario')", name="ck_usuario_perfil"),
    )

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, default="voluntario")
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    def definir_senha(self, senha: str) -> None:
        """Armazena somente o hash da senha, nunca seu texto original."""
        if not senha:
            raise ValueError("A senha não pode estar vazia.")
        self.senha_hash = generate_password_hash(senha, method="scrypt")

    def verificar_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)


class Produto(db.Model):
    """Alimento ou outro item controlado no estoque."""

    __tablename__ = "produtos"
    __table_args__ = (
        CheckConstraint("quantidade_estoque >= 0", name="ck_produto_estoque_nao_negativo"),
    )

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(80), nullable=False)
    unidade_medida = db.Column(db.String(30), nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False, default=0)
    ativo = db.Column(db.Boolean, nullable=False, default=True)


class Doacao(db.Model):
    """Entrada de alimento registrada por usuário autorizado."""

    __tablename__ = "doacoes"
    __table_args__ = (
        CheckConstraint("quantidade > 0", name="ck_doacao_quantidade_positiva"),
    )

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    registrado_por = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime(timezone=True), nullable=False)

    produto = db.relationship("Produto", backref="doacoes")
    usuario = db.relationship("Usuario", backref="doacoes_registradas")
