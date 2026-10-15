"""Métricas comuns ao painel da loja e às tools MCP."""
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from banco import conectar, agora, iso


def reais(centavos):
    return float((Decimal(centavos) / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def janela(horas):
    if type(horas) is not int or not 1 <= horas <= 8760:
        raise ValueError("O período deve ter de 1 a 8760 horas.")
    fim = agora()
    return iso(fim - timedelta(hours=horas)), iso(fim)


def listar_produtos(categoria=None):
    with conectar() as conn:
        linhas = conn.execute("SELECT * FROM produtos WHERE (? IS NULL OR categoria=?) ORDER BY id", (categoria, categoria)).fetchall()
    return [{**dict(p), "preco_reais": reais(p["preco_centavos"])} for p in linhas]


def produtos_mais_vendidos(limite=5, horas=168):
    if type(limite) is not int or not 1 <= limite <= 20:
        raise ValueError("O limite deve ser de 1 a 20 produtos.")
    inicio, fim = janela(horas)
    with conectar() as conn:
        linhas = conn.execute("""
        SELECT p.id AS produto_id, p.nome, SUM(i.quantidade) AS unidades,
        SUM(i.quantidade * i.preco_unitario_centavos) AS receita_centavos
        FROM itens_pedido i JOIN pedidos v ON v.id=i.pedido_id JOIN produtos p ON p.id=i.produto_id
        WHERE v.criado_em >= ? AND v.criado_em <= ?
        GROUP BY p.id,p.nome ORDER BY unidades DESC, receita_centavos DESC, p.id ASC LIMIT ?
        """, (inicio, fim, limite)).fetchall()
    return {"inicio_utc": inicio, "fim_utc": fim, "horas": horas, "criterio": "unidades vendidas, desempate por receita e ID", "produtos": [{**dict(p), "receita_reais": reais(p["receita_centavos"])} for p in linhas]}


def valor_medio(horas=24):
    inicio, fim = janela(horas)
    with conectar() as conn:
        n, total = conn.execute("SELECT COUNT(*),COALESCE(SUM(total_centavos),0) FROM pedidos WHERE criado_em>=? AND criado_em<=?", (inicio, fim)).fetchone()
        unidades, receita_itens = conn.execute("SELECT COALESCE(SUM(i.quantidade),0), COALESCE(SUM(i.quantidade*i.preco_unitario_centavos),0) FROM itens_pedido i JOIN pedidos p ON p.id=i.pedido_id WHERE p.criado_em>=? AND p.criado_em<=?", (inicio, fim)).fetchone()
        precos, produtos = conn.execute("SELECT SUM(preco_centavos), COUNT(*) FROM produtos").fetchone()
    return {"inicio_utc": inicio, "fim_utc": fim, "horas": horas, "pedidos": n,
            "ticket_medio_reais": reais(Decimal(total) / n) if n else None,
            "preco_medio_catalogo_reais": reais(Decimal(precos) / produtos) if produtos else None,
            "preco_medio_unidade_vendida_reais": reais(Decimal(receita_itens) / unidades) if unidades else None,
            "definicoes": {"ticket_medio": "Receita do período dividida pelo número de pedidos.", "preco_medio_catalogo": "Média dos preços atuais dos produtos, sem ponderar vendas.", "preco_medio_unidade_vendida": "Receita dos itens do período dividida pelas unidades vendidas."}}


def vendas_ultimas_24h():
    inicio, fim = janela(24)
    with conectar() as conn:
        n, total = conn.execute("SELECT COUNT(*),COALESCE(SUM(total_centavos),0) FROM pedidos WHERE criado_em>=? AND criado_em<=?", (inicio, fim)).fetchone()
        unidades = conn.execute("SELECT COALESCE(SUM(i.quantidade),0) FROM itens_pedido i JOIN pedidos p ON p.id=i.pedido_id WHERE p.criado_em>=? AND p.criado_em<=?", (inicio, fim)).fetchone()[0]
        recentes = conn.execute("SELECT id,criado_em,total_centavos FROM pedidos WHERE criado_em>=? AND criado_em<=? ORDER BY criado_em DESC,id DESC LIMIT 10", (inicio, fim)).fetchall()
    return {"inicio_utc": inicio, "fim_utc": fim, "horas": 24, "pedidos": n, "unidades": unidades,
            "receita_centavos": total, "receita_reais": reais(total), "ticket_medio_reais": reais(Decimal(total) / n) if n else None,
            "pedidos_recentes": [{**dict(p), "total_reais": reais(p["total_centavos"])} for p in recentes],
            "ficticio": True}
