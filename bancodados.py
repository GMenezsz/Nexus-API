import sqlite3

transacoes = """
    CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    tipo TEXT NOT NULL, 
    categoria TEXT NOT NULL,
    valor REAL NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
)"""

usuario = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        sobrenome TEXT NOT NULL
    )
"""

def criar_banco():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(usuario)
    cursor.execute(transacoes)
    conn.commit()
    conn.close()

def verificar_usuario(nome):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def inserir_usuario(nome, sobrenome):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, sobrenome) VALUES (?, ?)", (nome, sobrenome))
    conn.commit()
    usuario_id = cursor.lastrowid
    conn.close()
    return usuario_id

def inserir_transacao(usuario_id, tipo, categoria, valor):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transacoes (usuario_id, tipo, categoria, valor) VALUES (?, ?, ?, ?)", 
        (usuario_id, tipo, categoria, valor)
    )
    conn.commit()
    conn.close()

def atualizar_transacao(id, tipo, categoria, valor):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE transacoes SET tipo = ?, categoria = ?, valor = ? WHERE id = ?", 
        (tipo, categoria, valor, id)
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