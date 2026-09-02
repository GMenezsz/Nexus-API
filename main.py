from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from autenticacoes import autenticar_nome, autenticar_sobrenome, autenticar_transacao, autenticar_categoria, CATEGORIAS_RECEITA, CATEGORIAS_DESPESA
from bancodados import criar_banco, transacoes, usuario, inserir_transacao, atualizar_transacao, deletar_transacao, listar_transacoes, verificar_usuario, inserir_usuario
from calculo import calcular_transacoes

app = FastAPI(title="App Finanças")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransacaoSchema(BaseModel):
    usuario_id: int
    tipo: str
    categoria: str
    valor: float

class UsuarioSchema(BaseModel):
    nome: str
    sobrenome: str

criar_banco()

@app.post("/login")
def fazer_login(dados: UsuarioSchema):

    if not autenticar_nome(dados.nome):
        raise HTTPException(status_code=400, detail="Nome inválido. Deve ter pelo menos 3 caracteres.")
    
    if not autenticar_sobrenome(dados.sobrenome):
        raise HTTPException(status_code=400, detail="Sobrenome inválido. Deve ter pelo menos 3 caracteres.")
    
    usuario_existente = verificar_usuario(dados.nome)

    if usuario_existente:
        usuario_id, nome, sobrenome = usuario_existente
    else:
        usuario_id = inserir_usuario(dados.nome, dados.sobrenome)
        nome = dados.nome
        sobrenome = dados.sobrenome

    return {"usuario_id": usuario_id,
            "nome": nome,
            "sobrenome": sobrenome,
            "mensagem": f"Olá, {nome}!"}

@app.get("/categorias")
def obter_categorias():
    """O front-end chama isso para montar o select de categorias
    de acordo com o tipo (receita ou despesa) escolhido pelo usuário."""
    return {
        "receita": CATEGORIAS_RECEITA,
        "despesa": CATEGORIAS_DESPESA,
    }

@app.post("/transacoes")
def criar_transacao(dados: TransacaoSchema):

    if not autenticar_transacao(dados.valor):
        raise HTTPException(status_code=400, detail="Valor da transação inválido. Deve ser maior ou igual a zero.")

    if not autenticar_categoria(dados.tipo, dados.categoria):
        raise HTTPException(
            status_code=400,
            detail=f"Categoria '{dados.categoria}' inválida para o tipo '{dados.tipo}'."
        )

    inserir_transacao(dados.usuario_id, dados.tipo, dados.categoria, dados.valor)
    return {"valor": dados.valor,
            "tipo": dados.tipo,
            "categoria": dados.categoria}

@app.get("/transacoes/{usuario_id}")
def obter_transacoes(usuario_id: int):
    dados = listar_transacoes(usuario_id)
    # dados vem como (id, usuario_id, tipo, categoria, valor)
    transacoes_lista = [
        {"id": t[0], "tipo": t[2], "categoria": t[3], "valor": t[4]} for t in dados
    ]
    return {"transacoes": transacoes_lista}

@app.get("/transacoes/{usuario_id}/resumo")
def obter_resumo(usuario_id: int):
    dados = listar_transacoes(usuario_id)
    # calcular_transacoes espera tuplas (tipo, categoria, valor)
    apenas_calculo = [(t[2], t[3], t[4]) for t in dados]
    return calcular_transacoes(apenas_calculo)

@app.delete("/transacoes/{id}")
def remover_transacao(id: int):
    deletar_transacao(id)
    return {"mensagem": "Transação removida."}

@app.get("/")
def raiz():
    return {"mensagem": "API do App Finanças está rodando!"}
