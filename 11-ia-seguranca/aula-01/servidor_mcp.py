from mcp.server.fastmcp import FastMCP
import banco

import consultas

banco.inicializar()
mcp = FastMCP("Mcp da loja")

@mcp.tool(description="Lista os produtos cadastrados na loja, com preço em reais.")
def produtos_mais_vendidos(horas:int = 24, limite:int =5) -> dict:
    """Retorna os produtos mais vendidos no período de horas, limitado a limite produtos."""
    consulta = consultas.produtos_mais_vendidos(limite=limite, horas=horas)
    return {"produtos": consulta}

@mcp.tool()
def valor_medio(horas:int =24)-> dict:
    """Retorna o valor médio dos pedidos, preço médio do catálogo e preço médio das unidades vendidas no período de horas."""
    consulta = consultas.valor_medio(horas=horas)
    return {"valor_medio": consulta}



mcp.run(transport="stdio")
