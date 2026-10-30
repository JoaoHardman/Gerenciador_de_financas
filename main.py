from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()
engine = create_engine("sqlite:///./financas.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="API Gerenciador de finanças", 
    description="API para gerenciamento financeiro pessoal", 
    version="1.0.0", 
    contact={"name": "João Pedro",
             "url": "https://github.com/JoaoHardman",
             "email": "jp.hardman.l@gmail.com"})


security = HTTPBasic()

user_correto = os.getenv("user_correto")
senha_correta = os.getenv("senha_correta")

def session_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def autenticar(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != user_correto or credentials.password != senha_correta:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos", headers={"WWW-Authenticate": "Basic"})

class MovimentacaoDB(Base):
    __tablename__ = "movimentacoes"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    valor = Column(Float, index=True)
    tipo = Column(String, index=True)
    categoria = Column(String, index=True)

Base.metadata.create_all(bind=engine)

class Movimentacao(BaseModel):
     descricao: str = Field(min_length=1)
     valor: float = Field(gt=0, description="Valor da movimentação deve ser maior que zero")
     tipo: Literal["receita", "despesa"]
     categoria: str = Field(min_length=1)
     
@app.get("/movimentacoes")
def get_movimentacoes(page: int = 1, limit: int = 10, db = Depends(session_db), credentials = Depends(autenticar)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Página e limite devem ser maiores que zero")

    movimentacoes = db.query(MovimentacaoDB).offset((page - 1) * limit).limit(limit).all()
    total_movimentacoes = db.query(MovimentacaoDB).count()
    return {"movimentacoes": [{"id": m.id, "descricao": m.descricao, "valor": m.valor, "tipo": m.tipo, "categoria": m.categoria} for m in movimentacoes], "page": page, "limit": limit, "total": total_movimentacoes}

@app.post("/movimentacoes")
def post_movimentacao(movimentacao: Movimentacao, credentials = Depends(autenticar), db = Depends(session_db)):
    tipo = movimentacao.tipo.strip().lower()
    if tipo not in ["receita", "despesa"]:
        raise HTTPException(status_code=400, detail="Tipo deve ser 'receita' ou 'despesa'")
    movimentacao_db = MovimentacaoDB(descricao=movimentacao.descricao, valor=movimentacao.valor, tipo=tipo, categoria=movimentacao.categoria)
    db.add(movimentacao_db)
    db.commit()
    db.refresh(movimentacao_db)
    return {"message": "Movimentação cadastrada com sucesso"}

@app.put("/movimentacoes/{id}")
def put_movimentacao(id: int, movimentacao: Movimentacao, credentials = Depends(autenticar), db = Depends(session_db)):
    tipo = movimentacao.tipo.strip().lower()
    if tipo not in ["receita", "despesa"]:
        raise HTTPException(status_code=400, detail="Tipo deve ser 'receita' ou 'despesa'")
    movimentacao_db = db.query(MovimentacaoDB).filter(MovimentacaoDB.id == id).first()
    if not movimentacao_db:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    db.query(MovimentacaoDB).filter(MovimentacaoDB.id == id).update({
        "descricao": movimentacao.descricao,
        "valor": movimentacao.valor,
        "tipo": movimentacao.tipo,
        "categoria": movimentacao.categoria
    })
    db.commit()
    return {"message": "Movimentação atualizada com sucesso"}

@app.delete("/movimentacoes/{id}")
def delete_movimentacao(id: int, credentials = Depends(autenticar), db = Depends(session_db)):

    movimentacao_db = db.query(MovimentacaoDB).filter(MovimentacaoDB.id == id).first()
    if not movimentacao_db:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    db.delete(movimentacao_db)
    db.commit()
    return {"message": "Movimentação deletada com sucesso"}