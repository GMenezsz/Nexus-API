import sqlite3

transacoes = """
    CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    tipo TEXT NOT NULL, 
    categoria TEXT NOT NULL,
    valor REAL NOT NULL,
    data TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pago',
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
)"""

usuario = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        sobrenome TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
"""

metas = """
    CREATE TABLE IF NOT EXISTS metas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    salario_liquido REAL NOT NULL,
    meta REAL NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
)"""

def criar_banco():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(usuario)
    cursor.execute(metas)
    cursor.execute(transacoes)
    conn.commit()
    conn.close()

def verificar_usuario(usuario):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, senha FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def buscar_id_por_usuario(usuario: str):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def buscar_senha_por_usuario(usuario: str):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, senha FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def inserir_usuario(nome, sobrenome, usuario, senha):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, sobrenome, usuario, senha) VALUES (?, ?, ?, ?)", (nome, sobrenome, usuario, senha))
    conn.commit()
    usuario_id = cursor.lastrowid
    conn.close()
    return usuario_id

def inserir_transacao(usuario_id, tipo, categoria, valor, data, status):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transacoes (usuario_id, tipo, categoria, valor, data, status) VALUES (?, ?, ?, ?, ?, ?)", 
        (usuario_id, tipo, categoria, valor, data, status)
    )
    conn.commit()
    conn.close()

def atualizar_transacao(id, tipo, categoria, valor, data, status):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE transacoes SET tipo = ?, categoria = ?, valor = ?, data = ?, status = ? WHERE id = ?", 
        (tipo, categoria, valor, data, status, id)
    )
    conn.commit()
    conn.close()

def deletar_transacao(id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def listar_transacoes(usuario_id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes WHERE usuario_id = ?", (usuario_id,))
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_usuario(id, nome, sobrenome):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET nome = ?, sobrenome = ? WHERE id = ?", 
        (nome, sobrenome, id)
    )
    conn.commit()
    conn.close()

def atualizar_senha(id, nova_senha):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET senha = ? WHERE id = ?", 
        (nova_senha, id)
    )
    conn.commit()
    conn.close()

def excluir_conta(usuario_id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conn.commit()
    conn.close()

def deletar_meta(usuario_id, titulo):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM metas WHERE usuario_id = ? AND titulo = ?", (usuario_id, titulo))
    conn.commit()
    conn.close()


def listar_metas(usuario_id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM metas WHERE usuario_id = ?", (usuario_id,))
    dados = cursor.fetchall()
    conn.close()
    return dados

def inserir_titulo_salario_e_meta(usuario_id, titulo, salario_liquido, meta):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO metas (usuario_id, titulo, salario_liquido, meta) VALUES (?, ?, ?, ?)", 
        (usuario_id, titulo, salario_liquido, meta)
    )
    conn.commit()
    conn.close()

def atualizar_titulo_salario_e_meta(usuario_id, titulo, salario_liquido, meta):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE metas SET titulo = ?, salario_liquido = ?, meta = ? WHERE usuario_id = ?", (titulo, salario_liquido, meta, usuario_id)
    )
    conn.commit()
    conn.close()

def reiniciar_dados_usuario(usuario_id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes WHERE usuario_id = ?", (usuario_id,))
    cursor.execute("DELETE FROM metas WHERE usuario_id = ?", (usuario_id,))
    conn.commit()
    conn.close()