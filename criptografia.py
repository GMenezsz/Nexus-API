import bcrypt

def criar_hash(senha):
    bytes_senha = senha.encode('utf-8') 
    return bcrypt.hashpw(bytes_senha, bcrypt.gensalt())  

def verificar_senha(senha_digitada, hash_salvo):
    bytes_tentativa = senha_digitada.encode('utf-8') 
    return bcrypt.checkpw(bytes_tentativa, hash_salvo)