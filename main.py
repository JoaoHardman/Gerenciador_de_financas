from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

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

user_correto = "admin"
senha_correta = "admin"

def session_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def autenticar(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != user_correto or credentials.password != senha_correta:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos", headers={"WWW-Authenticate": "Basic"})

class movimentacaoDB(Base):
    __tablename__ = "movimentacoes"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    valor = Column(Float, index=True)
    tipo = Column(String, index=True)
    categoria = Column(String, index=True)

Base.metadata.create_all(bind=engine)

class Movimentacao(BaseModel):
     descricao: str
     valor: float
     tipo: str
     categoria: str
     
@app.get("/movimentacoes")
def get_movimentacoes(page: int = 1, limit: int = 10, db = Depends(session_db), credentials: HTTPBasicCredentials = Depends(security)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Página e limite devem ser maiores que zero")

    movimentacoes = db.query(movimentacaoDB).offset((page - 1) * limit).limit(limit).all()
    if not movimentacoes:
        raise HTTPException(status_code=404, detail="Nenhuma movimentação encontrada")
    total_movimentacoes = db.query(movimentacaoDB).count()
    return {"movimentacoes": [{"id": m.id, "descricao": m.descricao, "valor": m.valor, "tipo": m.tipo, "categoria": m.categoria} for m in movimentacoes], "page": page, "limit": limit, "total": total_movimentacoes}

@app.post("/movimentacoes")
def post_movimentacao(movimentacao: Movimentacao, credentials: HTTPBasicCredentials = Depends(security), db = Depends(session_db)):
    movimentacao_db = movimentacaoDB(descricao=movimentacao.descricao, valor=movimentacao.valor, tipo=movimentacao.tipo, categoria=movimentacao.categoria)
    db.add(movimentacao_db)
    db.commit()
    db.refresh(movimentacao_db)
    return {"message": "Movimentação cadastrada com sucesso"}

@app.put("/movimentacoes/{id}")
def put_movimentacao(id: int, movimentacao: Movimentacao, credentials: HTTPBasicCredentials = Depends(security), db = Depends(session_db)):

    movimentacao_db = db.query(movimentacaoDB).filter(movimentacaoDB.id == id).first()
    if not movimentacao_db:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    db.query(movimentacaoDB).filter(movimentacaoDB.id == id).update({
        "descricao": movimentacao.descricao,
        "valor": movimentacao.valor,
        "tipo": movimentacao.tipo,
        "categoria": movimentacao.categoria
    })
    db.commit()
    return {"message": "Movimentação atualizada com sucesso"}

@app.delete("/movimentacoes/{id}")
def delete_movimentacao(id: int, credentials: HTTPBasicCredentials = Depends(security), db = Depends(session_db)):

    movimentacao_db = db.query(movimentacaoDB).filter(movimentacaoDB.id == id).first()
    if not movimentacao_db:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    db.delete(movimentacao_db)
    db.commit()
    return {"message": "Movimentação deletada com sucesso"}