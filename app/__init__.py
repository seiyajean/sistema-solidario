"""Fábrica de aplicação do Sistema Solidário."""

import os
from pathlib import Path

from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import click


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(test_config=None):
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)

    app.config.from_mapping(
        if os.environ.get("FLASK_ENV_MODE") == "production":
    if not os.environ.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY obrigatória em produção."
        )
        SECRET_KEY=(
    os.environ.get("SECRET_KEY")
    or (
        "dev-only-change-me"
        if os.environ.get("FLASK_ENV_MODE", "development") == "development"
        else None
        )
    ),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL", f"sqlite:///{instance_path / 'sistema_solidario.db'}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "web.login"
    login_manager.login_message = "Entre para acessar o sistema."

    from app.models import Usuario

    @login_manager.user_loader
    def load_user(usuario_id):
        try:
            usuario = db.session.get(Usuario, int(usuario_id))
            return usuario if usuario and usuario.ativo else None
        except (ValueError, TypeError):
            return None

    from app.web import web
    app.register_blueprint(web)

    # Importa os modelos para registrá-los no metadata do SQLAlchemy.
    from app import models  # noqa: F401

    @app.cli.command("init-db")
    def init_db():
        """Cria as tabelas do banco configurado (uso inicial/local)."""
        db.create_all()
        print("Tabelas do Sistema Solidário criadas.")

    @app.cli.command("criar-gestor")
    @click.option("--nome", prompt=True)
    @click.option("--email", prompt=True)
    @click.password_option("--senha", confirmation_prompt=True)
    def criar_gestor_cli(nome, email, senha):
        """Cria primeiro gestor localmente sem senha fixa no código."""
        from app.models import Usuario
        email = email.strip().lower()
        if db.session.execute(db.select(Usuario).filter_by(email=email)).scalar_one_or_none():
            raise click.ClickException("Este e-mail já está cadastrado.")
        usuario = Usuario(nome=nome.strip(), email=email, perfil="gestor", ativo=True)
        usuario.definir_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        click.echo("Gestor criado com sucesso.")

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

    @app.get("/health")
    def health():
        return {"status": "ok", "app": "sistema-solidario"}, 200

    return app
