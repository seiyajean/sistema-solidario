"""Testes de interface e autenticação do MVP."""
import pytest
from app import create_app, db
from app.models import Usuario, Produto

@pytest.fixture
def ambiente(tmp_path):
    app = create_app({"TESTING": True, "SECRET_KEY": "chave-de-testes", "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'web.db'}", "WTF_CSRF_ENABLED": False})
    with app.app_context():
        db.create_all()
        usuario = Usuario(nome="Gestora Teste", email="gestora@teste.org", perfil="gestor", ativo=True)
        usuario.definir_senha("senha-segura-123")
        db.session.add(usuario)
        db.session.commit()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def entrar(cliente):
    return cliente.post("/login", data={"email": "gestora@teste.org", "senha": "senha-segura-123"}, follow_redirects=True)

def test_login_exige_credenciais(ambiente):
    assert ambiente.get("/dashboard").status_code == 302
    assert b"Credenciais" in ambiente.post("/login", data={"email":"gestora@teste.org","senha":"errada"}, follow_redirects=True).data

def test_painel_e_cadastro(ambiente):
    assert entrar(ambiente).status_code == 200
    r = ambiente.post("/produtos", data={"nome":"Arroz", "categoria":"Graos", "unidade_medida":"pacote"}, follow_redirects=True)
    assert r.status_code == 200
    assert b"Arroz" in r.data

def test_doacao_e_distribuicao(ambiente):
    entrar(ambiente)
    ambiente.post("/produtos", data={"nome":"Feijao", "categoria":"Graos", "unidade_medida":"pacote"})
    assert b"Doa" in ambiente.post("/doacoes", data={"produto_id":"1", "quantidade":"10"}, follow_redirects=True).data
    assert b"10 pacote" in ambiente.get("/dashboard").data
    ambiente.post("/distribuicoes", data={"produto_id":"1", "quantidade":"3"})
    assert b"7 pacote" in ambiente.get("/dashboard").data
    assert b"Estoque insuficiente" in ambiente.post("/distribuicoes", data={"produto_id":"1", "quantidade":"100"}, follow_redirects=True).data
    assert b"7 pacote" in ambiente.get("/dashboard").data
