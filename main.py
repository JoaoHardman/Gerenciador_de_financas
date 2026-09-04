from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI(title="API Gerenciador de finanças", 
    description="API para gerenciamento financeiro pessoal", 
    version="1.0.0", 
    contact={"name": "João Pedro",
             "url": "https://github.com/JoaoHardman",
             "email": "jp.hardman.l@gmail.com"})


security = HTTPBasic()

user_correto = "admin"
senha_correta = "admin"

def autenticar(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != user_correto or credentials.password != senha_correta:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos", headers={"WWW-Authenticate": "Basic"})

class Movimentacao(BaseModel):
     descricao: str
     valor: float
     tipo: str
     categoria: str
     
movimentacoes = {}
proximo_id = 1

@app.get("/movimentacoes")
def get_movimentacoes(page: int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(security)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Página e limite devem ser maiores que zero")
    if not movimentacoes:
        raise HTTPException(status_code=404, detail="Nenhuma movimentação encontrada")
    start = (page - 1) * limit
    end = start + limit
    movimentacoes_paginadas = list(movimentacoes.values())[start:end]
    return {"movimentacoes": movimentacoes_paginadas, "page": page, "limit": limit, "total": len(movimentacoes)}

@app.post("/movimentacoes")
def post_movimentacao(movimentacao: Movimentacao, credentials: HTTPBasicCredentials = Depends(security)):

    global proximo_id
    if movimentacao.valor <= 0:
        raise HTTPException(status_code=400, detail="O valor deve ser maior que zero")
    if movimentacao.tipo not in ["receita", "despesa"]:
        raise HTTPException(status_code=400, detail="O tipo deve ser 'receita' ou 'despesa'")
    if not movimentacao.descricao.strip():
        raise HTTPException(status_code=400, detail="A descrição não pode estar vazia")
    movimentacoes[proximo_id] = {"id": proximo_id, **movimentacao.model_dump()}
    proximo_id += 1
    return {"message": "Movimentação cadastrada com sucesso"}

@app.put("/movimentacoes/{id}")
def put_movimentacao(id: int, movimentacao: Movimentacao, credentials: HTTPBasicCredentials = Depends(security)):

    if id not in movimentacoes:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    if movimentacao.valor <= 0:
        raise HTTPException(status_code=400, detail="O valor deve ser maior que zero")
    if movimentacao.tipo not in ["receita", "despesa"]:
        raise HTTPException(status_code=400, detail="O tipo deve ser 'receita' ou 'despesa'")
    if not movimentacao.descricao.strip():
        raise HTTPException(status_code=400, detail="A descrição não pode estar vazia")
    movimentacoes[id] = movimentacao.model_dump()
    return {"message": "Movimentação atualizada com sucesso"}

@app.delete("/movimentacoes/{id}")
def delete_movimentacao(id: int, credentials: HTTPBasicCredentials = Depends(security)):

    if id not in movimentacoes:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    del movimentacoes[id]
    return {"message": "Movimentação removida com sucesso"}
