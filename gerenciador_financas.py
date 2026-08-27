from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="API Gerenciador de finanças", 
    description="API para gerenciamento financeiro pessoal", 
    version="1.0.0", 
    contact={"name": "João Pedro",
             "url": "https://github.com/JoaoHardman",
             "email": "jp.hardman.l@gmail.com"})

class Movimentacao(BaseModel):
     descricao: str
     valor: float
     tipo: str
     categoria: str
     
movimentacoes = {}
proximo_id = 1

@app.get("/movimentacoes")
def get_movimentacoes():

    if not movimentacoes:
        raise HTTPException(status_code=404, detail='Sem movimentações cadastradas!')

    return {"movimentacoes": movimentacoes}

@app.post("/movimentacoes")
def post_movimentacao(movimentacao: Movimentacao):

    global proximo_id
    if movimentacao.valor <= 0:
        raise HTTPException(status_code=400, detail="O valor deve ser maior que zero")
    if movimentacao.tipo not in ["receita", "despesa"]:
        raise HTTPException(status_code=400, detail="O tipo deve ser 'receita' ou 'despesa'")
    if not movimentacao.descricao.strip():
        raise HTTPException(status_code=400, detail="A descrição não pode estar vazia")
    movimentacoes[proximo_id] = movimentacao.model_dump()
    proximo_id += 1
    return {"message": "Movimentação cadastrada com sucesso"}

@app.put("/movimentacoes/{id}")
def put_movimentacao(id: int, movimentacao: Movimentacao):

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
def delete_movimentacao(id: int):

    if id not in movimentacoes:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    del movimentacoes[id]
    return {"message": "Movimentação removida com sucesso"}
