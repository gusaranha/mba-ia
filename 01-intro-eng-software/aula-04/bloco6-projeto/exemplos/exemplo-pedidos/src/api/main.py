from fastapi import FastAPI, HTTPException
from src.models.schemas import PedidoRequest, PedidoResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema de Pedidos")

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/calcular", response_model=PedidoResponse)
def calcular_pedido(pedido: PedidoRequest):
    """Calcula total do pedido com desconto opcional"""
    try:
        # Calcula subtotal
        subtotal = sum(item.preco * item.quantidade for item in pedido.itens)
        
        # Aplica desconto se tiver cupom DESC10
        desconto = subtotal * 0.10 if pedido.cupom == "DESC10" else 0
        
        total = subtotal - desconto
        
        logger.info(f"Pedido calculado: subtotal={subtotal}, desconto={desconto}, total={total}")
        
        return PedidoResponse(
            subtotal=round(subtotal, 2),
            desconto=round(desconto, 2),
            total=round(total, 2)
        )
        
    except Exception as e:
        logger.error(f"Erro ao calcular pedido: {e}")
        raise HTTPException(status_code=500, detail=str(e))
