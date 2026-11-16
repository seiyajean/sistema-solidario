"""Rotas web autenticadas do MVP Sistema Solidário."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Email
from sqlalchemy import func
from app import db
from app.models import Usuario, Produto, Doacao, Distribuicao
from app.doacoes import registrar_doacao
from app.distribuicoes import registrar_distribuicao

web = Blueprint("web", __name__)

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=254)])
    senha = PasswordField("Senha", validators=[DataRequired()])

class ProdutoForm(FlaskForm):
    nome = StringField("Nome do alimento", validators=[DataRequired(), Length(max=120)])
    categoria = StringField("Categoria", validators=[DataRequired(), Length(max=80)])
    unidade_medida = SelectField("Unidade de medida", choices=[("unidade", "Unidade"), ("kg", "Quilograma"), ("pacote", "Pacote"), ("litro", "Litro")])

class MovimentoForm(FlaskForm):
    produto_id = SelectField("Alimento", coerce=int, validators=[DataRequired()])
    quantidade = IntegerField("Quantidade", validators=[DataRequired(), NumberRange(min=1)])

@web.get("/")
def inicio():
    return redirect(url_for("web.dashboard" if current_user.is_authenticated else "web.login"))

@web.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("web.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = db.session.execute(db.select(Usuario).filter_by(email=form.email.data.strip().lower(), ativo=True)).scalar_one_or_none()
        if usuario and usuario.verificar_senha(form.senha.data):
            login_user(usuario)
            return redirect(url_for("web.dashboard"))
        flash("Credenciais inválidas.", "erro")
    return render_template("login.html", form=form)

@web.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Sessão encerrada.", "sucesso")
    return redirect(url_for("web.login"))

@web.get("/dashboard")
@login_required
def dashboard():
    produtos = db.session.execute(db.select(Produto).filter_by(ativo=True).order_by(Produto.nome)).scalars().all()
    total = sum(p.quantidade_estoque for p in produtos)
    doacoes = db.session.scalar(db.select(func.count(Doacao.id))) or 0
    distribuicoes = db.session.scalar(db.select(func.count(Distribuicao.id))) or 0
    return render_template("dashboard.html", produtos=produtos, total=total, doacoes=doacoes, distribuicoes=distribuicoes)

@web.route("/produtos", methods=["GET", "POST"])
@login_required
def produtos():
    form = ProdutoForm()
    if form.validate_on_submit():
        if current_user.perfil != "gestor":
            abort(403)
        produto = Produto(nome=form.nome.data.strip(), categoria=form.categoria.data.strip(), unidade_medida=form.unidade_medida.data, quantidade_estoque=0, ativo=True)
        db.session.add(produto)
        db.session.commit()
        flash("Alimento cadastrado com sucesso.", "sucesso")
        return redirect(url_for("web.produtos"))
    itens = db.session.execute(db.select(Produto).order_by(Produto.nome)).scalars().all()
    return render_template("produtos.html", form=form, produtos=itens)

def movimento(tipo):
    form = MovimentoForm()
    ativos = db.session.execute(db.select(Produto).filter_by(ativo=True).order_by(Produto.nome)).scalars().all()
    form.produto_id.choices = [(p.id, f"{p.nome} ({p.quantidade_estoque} {p.unidade_medida})") for p in ativos]
    if form.validate_on_submit():
        try:
            if tipo == "doacao":
                registrar_doacao(produto_id=form.produto_id.data, usuario_id=current_user.id, quantidade=form.quantidade.data)
                flash("Doação registrada e estoque atualizado.", "sucesso")
            else:
                registrar_distribuicao(produto_id=form.produto_id.data, usuario_id=current_user.id, quantidade=form.quantidade.data)
                flash("Distribuição registrada e estoque atualizado.", "sucesso")
            return redirect(url_for("web.dashboard"))
        except ValueError as erro:
            flash(str(erro), "erro")
    return render_template("movimento.html", form=form, tipo=tipo)

@web.route("/doacoes", methods=["GET", "POST"])
@login_required
def doacoes():
    return movimento("doacao")

@web.route("/distribuicoes", methods=["GET", "POST"])
@login_required
def distribuicoes():
    return movimento("distribuicao")

@web.get("/historico")
@login_required
def historico():
    entradas = db.session.execute(db.select(Doacao).order_by(Doacao.data.desc()).limit(50)).scalars().all()
    saidas = db.session.execute(db.select(Distribuicao).order_by(Distribuicao.data.desc()).limit(50)).scalars().all()
    registros = sorted([("Doação", x) for x in entradas] + [("Distribuição", x) for x in saidas], key=lambda r: r[1].data, reverse=True)
    return render_template("historico.html", registros=registros)
