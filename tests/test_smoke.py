"""Verificações iniciais de disponibilidade da aplicação."""
from app import create_app



def test_pagina_inicial():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only"
    })

    resposta = app.test_client().get("/")

    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_health():
    app = create_app({"TESTING": True, "SECRET_KEY": "test-only"})
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
