from fastapi import FastAPI, HTTPException

app = FastAPI()

tarefas = {}

@app.get("/tarefas")
def get_tarefas():
    if not tarefas:
        return {'message': 'Não existem tarefas cadastradas'}
    else:
        return {'tarefas': tarefas}

@app.post("/tarefas")
def post_tarefas(nome: str, descricao: str):
    if nome in tarefas:
        raise HTTPException(status_code=400, detail="Tarefa já cadastrada")
    else:
        tarefas[nome] = {'descricao': descricao, 'status': False}
        return {'message': 'Tarefa adicionada com sucesso'}

@app.put("/tarefas/{nome}")
def put_tarefas(nome: str, status: bool):
    if nome not in tarefas:
        raise HTTPException(status_code=404, detail='Tarefa não cadastrada!')
    else:
        tarefas[nome]["status"] = status
        return {'message': 'Tarefa atualizada com sucesso!'}

@app.delete("/tarefas/{nome}")
def delete_tarefas(nome):
    if nome not in tarefas:
        raise HTTPException(status_code=404, detail='Tarefa não cadastrada')
    del tarefas[nome]
    return {'message': 'Tarefa deletada com sucesso'}
