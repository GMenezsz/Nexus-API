from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from bancodados import listar_metas, inserir_titulo_salario_e_meta, atualizar_titulo_salario_e_meta, deletar_meta, buscar_id_por_usuario
from autenticacoes import salario_liquido, meta_valida

router = APIRouter(prefix="/metas", tags=["Metas"])

class MetaSchema(BaseModel):
    usuario: str
    titulo: str
    salario_liquido: float
    porcentagem_meta: float

class AtualizarMetaSchema(BaseModel):
    usuario: str
    titulo_antigo: str
    titulo_novo: str
    salario_liquido: float
    porcentagem_meta: float

@router.post("/criar")
def criar_meta(dados: MetaSchema):
    usuario_id = buscar_id_por_usuario(dados.usuario.strip().lower())
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    titulo_formatado = dados.titulo.strip().title()

    if not salario_liquido(dados.salario_liquido):
        raise HTTPException(status_code=400, detail="Salário líquido inválido. Deve ser maior que zero.")

    if not meta_valida(dados.porcentagem_meta):
        raise HTTPException(status_code=400, detail="Porcentagem da meta inválida. Deve ser maior que zero.")

    meta = dados.salario_liquido * (dados.porcentagem_meta / 100)
    inserir_titulo_salario_e_meta(usuario_id, titulo_formatado, dados.salario_liquido, meta)
    
    return {
        "mensagem": "Meta criada com sucesso!",
        "usuario": dados.usuario,
        "titulo": titulo_formatado,
        "salario_liquido": dados.salario_liquido,
        "valor_objetivo": meta,
        "porcentagem": dados.porcentagem_meta,
    }

@router.put("/atualizar")
def atualizar_meta(dados: AtualizarMetaSchema):
    usuario_id = buscar_id_por_usuario(dados.usuario.strip().lower())
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    # Primeiro deleta a meta antiga
    deletar_meta(usuario_id, dados.titulo_antigo.strip().title())
    
    # Depois cria a nova
    titulo_formatado = dados.titulo_novo.strip().title()

    if not salario_liquido(dados.salario_liquido):
        raise HTTPException(status_code=400, detail="Salário líquido inválido. Deve ser maior que zero.")

    if not meta_valida(dados.porcentagem_meta):
        raise HTTPException(status_code=400, detail="Porcentagem da meta inválida. Deve ser maior que zero.")

    meta = dados.salario_liquido * (dados.porcentagem_meta / 100)
    inserir_titulo_salario_e_meta(usuario_id, titulo_formatado, dados.salario_liquido, meta)

    return {
        "mensagem": "Meta atualizada com sucesso!",
        "usuario": dados.usuario,
        "titulo": titulo_formatado,
        "salario_liquido": dados.salario_liquido,
        "valor_objetivo": meta,
        "porcentagem": dados.porcentagem_meta,
    }

@router.get("/listar")
def obter_metas(usuario: str):
    usuario_id = buscar_id_por_usuario(usuario.strip().lower())
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    dados = listar_metas(usuario_id)
    metas_lista = [
        {
            "id": m[0],
            "usuario_id": m[1],
            "titulo": m[2],
            "salario_liquido": m[3],
            "meta": m[4]
        } for m in dados
    ]
    return {"metas": metas_lista}

@router.delete("/deletar")
def excluir_meta(usuario: str, titulo: str):
    usuario_id = buscar_id_por_usuario(usuario.strip().lower())
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    deletar_meta(usuario_id, titulo.strip().title())
    return {"mensagem": f"Meta '{titulo}' excluída com sucesso."}