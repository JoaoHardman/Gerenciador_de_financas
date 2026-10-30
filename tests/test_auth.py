import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app, Base, session_db
from dotenv import load_dotenv

load_dotenv()

print("Usuário carregado:", os.getenv("user_correto"))
print("Senha configurada:", os.getenv("senha_correta") is not None)

@pytest.fixture
def client():
    # Cria um banco SQLite temporário em memória.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    # Cria as tabelas no banco de testes.
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    # Substitui a conexão original pelo banco de testes.
    def override_session_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[session_db] = override_session_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        # Remove a substituição após cada teste.
        app.dependency_overrides.pop(session_db, None)
        engine.dispose()

def test_autenticacao_valida(client):
    usuario = os.environ["user_correto"]
    senha = os.environ["senha_correta"]
    response = client.get("/movimentacoes", auth=(usuario, senha))
    assert response.status_code == 200, (f"Esperado HTTP 200, recebido {response.status_code}")

def test_senha_incorreta(client):
    usuario = os.environ["user_correto"]
    senha = os.environ["senha_correta"]
    response = client.get("/movimentacoes", auth=(usuario, senha + "_incorreta"))
    assert response.status_code == 401, ("A API deveria rejeitar uma senha incorreta")

def test_usuario_incorreto(client):
    usuario = os.environ["user_correto"]
    senha = os.environ["senha_correta"]
    response = client.get("/movimentacoes", auth=(usuario + "_incorreto", senha))
    assert response.status_code == 401, ("A API deveria rejeitar um usuário incorreto")

def test_sem_credenciais(client):
    response = client.get("/movimentacoes")
    assert response.status_code == 401, ("A API deveria rejeitar requisições sem credenciais")