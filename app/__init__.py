"""Fábrica de aplicação do Sistema Solidário."""

import os
from pathlib import Path

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import click


db = SQLAlchemy()


def create_app(test_config=None):
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL", f"sqlite:///{instance_path / 'sistema_solidario.db'}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)

    # Importa os modelos para registrá-los no metadata do SQLAlchemy.
    from app import models  # noqa: F401

    @app.cli.command("init-db")
    def init_db():
        """Cria as tabelas do banco configurado (uso inicial/local)."""
        db.create_all()
        print("Tabelas do Sistema Solidário criadas.")

    @app.cli.command("registrar-doacao")
    @click.option("--produto", "produto_id", type=int, required=True)
    @click.option("--usuario", "usuario_id", type=int, required=True)
    @click.option("--quantidade", type=int, required=True)
    def registrar_doacao_cli(produto_id, usuario_id, quantidade):
        """Registra uma doação localmente (não expõe rota HTTP sem login)."""
        from app.doacoes import registrar_doacao
        try:
            doacao = registrar_doacao(
                produto_id=produto_id, usuario_id=usuario_id, quantidade=quantidade
            )
        except ValueError as erro:
            raise click.ClickException(str(erro)) from erro
        click.echo(f"Doação {doacao.id} registrada: {quantidade} unidade(s).")

    @app.cli.command("registrar-distribuicao")
    @click.option("--produto", "produto_id", type=int, required=True)
    @click.option("--usuario", "usuario_id", type=int, required=True)
    @click.option("--quantidade", type=int, required=True)
    def registrar_distribuicao_cli(produto_id, usuario_id, quantidade):
        """Registra saída localmente; não expõe rota HTTP sem autenticação."""
        from app.distribuicoes import registrar_distribuicao
        try:
            distribuicao = registrar_distribuicao(
                produto_id=produto_id, usuario_id=usuario_id, quantidade=quantidade
            )
        except ValueError as erro:
            raise click.ClickException(str(erro)) from erro
        click.echo(f"Distribuição {distribuicao.id} registrada: {quantidade} unidade(s).")

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return {"status": "ok", "app": "sistema-solidario"}, 200

    return app
