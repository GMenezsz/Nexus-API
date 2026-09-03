from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from bancodados import verificar_usuario, inserir_usuario, atualizar_usuario, excluir_conta, reiniciar_dados_usuario, buscar_id_por_usuario, atualizar_senha, buscar_senha_por_usuario
from autenticacoes import autenticar_nome, autenticar_sobrenome, autenticar_usuario, autenticar_senha

from criptografia import criar_hash, verificar_senha

router = APIRouter(tags=["Usuários"])

class LoginSchema(BaseModel):
    usuario: str
    senha: str

class UsuarioSchema(BaseModel):
    nome: str
    sobrenome: str
    usuario: str
    senha: str

class AtualizarNomeSchema(BaseModel):
    usuario: str
    nome: str
    sobrenome: str

class RecuperarSenhaSchema(BaseModel):
    usuario: str
    nova_senha: str

class AtualizarSenhaSchema(BaseModel):
    usuario: str
    senha_antiga: str
    nova_senha: str

@router.post("/criar_conta")
def cadastrar_usuario(dados: UsuarioSchema):

    nome_formatado = dados.nome.strip().title()
    sobrenome_formatado = dados.sobrenome.strip().title()
    usuario_formatado = dados.usuario.strip().lower()

    if not autenticar_nome(nome_formatado) or not autenticar_sobrenome(sobrenome_formatado):
        raise HTTPException(status_code=400, detail="Nome ou sobrenome inválidos.")

    if not autenticar_usuario(usuario_formatado) or not autenticar_senha(dados.senha):
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos.")

    if verificar_usuario(usuario_formatado):
        raise HTTPException(status_code=400, detail="Usuário já existe.")

    senha = criar_hash(dados.senha)
    inserir_usuario(nome_formatado, sobrenome_formatado, usuario_formatado, senha)

    return {"mensagem": "Usuário cadastrado com sucesso!", "usuario": usuario_formatado}

@router.post("/login")
def fazer_login(dados: LoginSchema):

    usuario_existente = verificar_usuario(dados.usuario.strip())
    
    if not usuario_existente or not verificar_senha(dados.senha, usuario_existente[1]):
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos.")
    
    nome = usuario_existente[0]
    return {
        "nome": nome,
        "boas_vindas": f"Olá, {nome}!"}

@router.put("/atualizar_nome_sobrenome")
def atualizar_usuario_endpoint(dados: AtualizarNomeSchema):

    usuario_formatado = dados.usuario.strip().lower()
    
    usuario_id = buscar_id_por_usuario(usuario_formatado)
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")

    nome_formatado = dados.nome.strip().title()
    sobrenome_formatado = dados.sobrenome.strip().title()

    atualizar_usuario(usuario_id, nome_formatado, sobrenome_formatado)
    return {"usuario": usuario_formatado, "nome": nome_formatado, "sobrenome": sobrenome_formatado}

@router.delete("/deletar_usuario")
def excluir_usuario_endpoint(usuario: str):
    
    usuario_formatado = usuario.strip().lower()
    usuario_id = buscar_id_por_usuario(usuario_formatado)
    
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    excluir_conta(usuario_id)
    return {"usuario": usuario_formatado, "mensagem": "Usuário excluído com sucesso."}

@router.delete("/reiniciar_conta")
def reiniciar_conta(usuario: str):
    usuario_formatado = usuario.strip().lower()
    usuario_id = buscar_id_por_usuario(usuario_formatado)
    
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    reiniciar_dados_usuario(usuario_id)
    return {"mensagem": "Dados do usuário reiniciados com sucesso."}

@router.put("/recuperar_senha")
def recuperar_senha_endpoint(dados: RecuperarSenhaSchema):

    usuario_id = buscar_id_por_usuario(dados.usuario.strip().lower())

    if not usuario_id:
        raise HTTPException(status_code=400, detail="Usuário não encontrado. Tente novamente.")

    senha = criar_hash(dados.nova_senha)
    atualizar_senha(usuario_id, senha)

    return {
        "mensagem": "Senha atualizada com sucesso!"
    }

@router.put("/atualizar_senha")
def atualizar_senha_endpoint(dados: AtualizarSenhaSchema):

    usuario_formatado = dados.usuario.strip().lower()

    usuario = buscar_senha_por_usuario(usuario_formatado)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado. Tente novamente.")

    usuario_id, senha_hash_atual = usuario

    if not verificar_senha(dados.senha_antiga, senha_hash_atual):
        raise HTTPException(status_code=400, detail="Senha antiga incorreta. Tente novamente.")

    nova_senha = criar_hash(dados.nova_senha)
    atualizar_senha(usuario_id, nova_senha)

    return {
        "mensagem": "Senha atualizada com sucesso!"
    }