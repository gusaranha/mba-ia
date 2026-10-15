from mcp.server.fastmcp import FastMCP
import banco

import consultas

banco.inicializar()
mcp = FastMCP("Mcp da loja")


@mcp.tool()
def listar_produtos(categoria: str | None = None) -> list[dict]:
    """Lista os produtos cadastrados na loja, com categoria e preço atual em reais. Filtra por categoria se informada."""
    return consultas.listar_produtos(categoria)


@mcp.tool()
def produtos_mais_vendidos(limite: int = 5, horas: int = 168) -> dict:
    """Ranking dos produtos mais vendidos por unidades nas últimas `horas` (1 a 8760), com até `limite` posições (1 a 20)."""
    return consultas.produtos_mais_vendidos(limite=limite, horas=horas)


@mcp.tool()
def valor_medio(horas: int = 24) -> dict:
    """Retorna o ticket médio dos pedidos, o preço médio do catálogo e o preço médio por unidade vendida nas últimas `horas`."""
    return consultas.valor_medio(horas=horas)


@mcp.tool()
def vendas_ultimas_24h() -> dict:
    """Retorna pedidos, unidades, receita fictícia, ticket médio e até dez pedidos recentes das últimas 24 horas."""
    return consultas.vendas_ultimas_24h()


mcp.run(transport="stdio")
