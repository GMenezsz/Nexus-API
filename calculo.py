def calcular_transacoes(transacoes):

    saldo = 0.0
    total_receitas = 0.0
    total_despesas = 0.0
    resumo_categoria = {}

    tipos_receita = ["receita", "entrada", "ganhos"]
    tipos_despesa = ["despesa", "saida", "saída", "gasto"]

    for tipo, categoria, valor in transacoes:
        resumo_categoria.setdefault(categoria, 0.0)

        if tipo.lower() in tipos_receita:
            saldo += valor
            total_receitas += valor
            resumo_categoria[categoria] += valor
        elif tipo.lower() in tipos_despesa:
            saldo -= valor
            total_despesas += valor
            resumo_categoria[categoria] -= valor

    return {
        "saldo": saldo,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "resumo_categoria": resumo_categoria,
    }