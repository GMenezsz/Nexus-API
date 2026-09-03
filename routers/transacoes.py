from datetime import date, timedelta
from fastapi import APIRouter, HTTPException

from pydantic import BaseModel, Field
from bancodados import inserir_transacao, atualizar_transacao, deletar_transacao, listar_transacoes, buscar_id_por_usuario

from autenticacoes import autenticar_transacao, autenticar_categoria, CATEGORIAS_RECEITA, CATEGORIAS_DESPESA
from calculo import calcular_transacoes

from typing import Optional

router = APIRouter(tags=["Transações"])

class TransacaoSchema(BaseModel):
    usuario: str
    tipo: str
    categoria: str
    valor: float
    data: Optional[str] = Field(default_factory=lambda: date.today().isoformat())
    status: str = "pago"

class AtualizarTransacaoSchema(BaseModel):
    usuario: str
    transacao_id: int
    tipo: str
    categoria: str
    valor: float
    data: Optional[str] = Field(default_factory=lambda: date.today().isoformat())
    status: str = "pago"

class DeletarTransacaoSchema(BaseModel):
    usuario: str
    transacao_id: int

@router.get("/categorias")
def obter_categorias():
    return {
        "receita": CATEGORIAS_RECEITA,
        "despesa": CATEGORIAS_DESPESA,
    }

@router.post("/transacoes/criar")
def criar_transacao(dados: TransacaoSchema):
    usuario_id = buscar_id_por_usuario(dados.usuario.strip().lower())
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    if not autenticar_transacao(dados.valor):
        raise HTTPException(status_code=400, detail="Valor da transação inválido.")

    if not autenticar_categoria(dados.tipo, dados.categoria):
        raise HTTPException(status_code=400, detail=f"Categoria '{dados.categoria}' inválida para o tipo '{dados.tipo}'.")

    inserir_transacao(usuario_id, dados.tipo, dados.categoria, dados.valor, dados.data, dados.status)
    return {
        "usuario": dados.usuario,
        "valor": dados.valor,
        "tipo": dados.tipo,
        "categoria": dados.categoria,
        "data": dados.data,
        "status": dados.status
    }

@router.get("/transacoes/listar")
def obter_transacoes(usuario: str):
    usuario_id = buscar_id_por_usuario(usuario.strip().lower())
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    dados = listar_transacoes(usuario_id)
    transacoes_lista = [
        {
            "id": t[0], "tipo": t[2], "categoria": t[3], 
            "valor": t[4], "data": t[5], "status": t[6]
        } for t in dados
    ]
    return {"transacoes": transacoes_lista}

@router.get("/transacoes/resumo")
def obter_resumo(usuario: str):
    usuario_id = buscar_id_por_usuario(usuario.strip().lower())
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    dados = listar_transacoes(usuario_id)
    return calcular_transacoes(dados)

@router.put("/transacoes/atualizar")
def atualizar_transacao_endpoint(dados: AtualizarTransacaoSchema):
    usuario_id = buscar_id_por_usuario(dados.usuario.strip().lower())
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    if not autenticar_transacao(dados.valor):
        raise HTTPException(status_code=400, detail="Valor inválido.")

    if not autenticar_categoria(dados.tipo, dados.categoria):
        raise HTTPException(status_code=400, detail="Categoria inválida.")

    atualizar_transacao(dados.transacao_id, dados.tipo, dados.categoria, dados.valor, dados.data, dados.status)
    return {
        "transacao_id": dados.transacao_id, 
        "valor": dados.valor, 
        "tipo": dados.tipo, 
        "categoria": dados.categoria, 
        "data": dados.data, 
        "status": dados.status
    }

@router.delete("/transacoes/deletar")
def deletar_transacao_endpoint(dados: DeletarTransacaoSchema):
    usuario_id = buscar_id_por_usuario(dados.usuario.strip().lower())
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    deletar_transacao(dados.transacao_id)
    return {"transacao_id": dados.transacao_id, "mensagem": "Transação excluída com sucesso."}