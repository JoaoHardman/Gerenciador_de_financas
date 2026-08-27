from fastapi import FastAPI, HTTPException

app = FastAPI()

movimentacoes = {}
proximo_id = 1

@app.get("/movimentacoes")
def get_movimentacoes():

    if not movimentacoes:
        raise HTTPException(status_code=404, detail='Sem movimentações cadastradas!')

    return {"movimentacoes": movimentacoes}

@app.post("/movimentacoes")
def post_movimentacao(descricao: str, valor: float, tipo: str, categoria: str):

    global proximo_id
    movimentacoes[proximo_id] = {"descricao": descricao, "valor": valor, "tipo": tipo, "categoria": categoria}
    proximo_id += 1
    return {"message": "Movimentação cadastrada com sucesso"}

@app.put("/movimentacoes/{id}")
def put_movimentacao(id: int, descricao: str, valor: float, tipo: str, categoria: str):

    if id not in movimentacoes:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    movimentacoes[id]["descricao"] = descricao
    movimentacoes[id]["valor"] = valor
    movimentacoes[id]["tipo"] = tipo
    movimentacoes[id]["categoria"] = categoria
    return {"message": "Movimentação atualizada com sucesso"}

@app.delete("/movimentacoes/{id}")
def delete_movimentacao(id: int):

    if id not in movimentacoes:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    del movimentacoes[id]
    return {"message": "Movimentação removida com sucesso"}
