def autenticar_nome(nome):
    if len(nome) >= 3:
        return True
    else:
        return False

def autenticar_sobrenome(sobrenome):
    if len(sobrenome) >= 3:
        return True
    else:
        return False

def autenticar_transacao(valor):
    if valor < 0:
        return False
    else:
        return True

CATEGORIAS_RECEITA = ["Salário", "Pix", "Bonificação", "Freelance", "Investimentos", "Outros"]
CATEGORIAS_DESPESA = ["Alimentação", "Transporte", "Moradia", "Lazer", "Contas", "Saúde", "Outros"]

TIPOS_RECEITA = ["receita", "entrada", "ganhos"]
TIPOS_DESPESA = ["despesa", "saida", "saída", "gasto"]

def autenticar_categoria(tipo, categoria):
    tipo = tipo.lower()
    if tipo in TIPOS_RECEITA:
        return categoria in CATEGORIAS_RECEITA
    elif tipo in TIPOS_DESPESA:
        return categoria in CATEGORIAS_DESPESA
    else:
        return False