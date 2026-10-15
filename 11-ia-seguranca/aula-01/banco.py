"""Banco SQLite compartilhado pelo site Flask e pelo servidor MCP."""
import os
import random
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("LOJA_DB", str(BASE / "dados" / "loja.sqlite3"))).resolve()

PRODUTOS = [
    (1, "Notebook Aurora 14", "Computadores", 429900, "notebook", "14 polegadas, 16 GB de RAM e SSD de 512 GB.", "Trabalho e estudo"),
    (2, "Fone Pulse sem fio", "Áudio", 24990, "fone", "Bluetooth, estojo compacto e até 24 horas de uso.", "Favorito da turma"),
    (3, "Monitor Vista 27", "Computadores", 119900, "monitor", "Tela de 27 polegadas, resolução QHD e conexão HDMI.", "Mais espaço"),
    (4, "Teclado mecânico Flux", "Acessórios", 32990, "teclado", "Layout ABNT2, iluminação suave e conexão USB.", "Mesa completa"),
    (5, "Mouse Orbit", "Acessórios", 12990, "mouse", "Sem fio, sensor preciso e bateria recarregável.", "Leve e preciso"),
    (6, "Caixa de som Wave", "Áudio", 39990, "caixa", "Som portátil, conexão Bluetooth e 12 horas de bateria.", "Som em todo lugar"),
    (7, "Smartphone Nova 128", "Celulares", 189900, "celular", "128 GB, tela de 6,5 polegadas e câmera de 50 MP.", "Todo dia"),
    (8, "Tablet Pixel 10", "Celulares", 149900, "tablet", "Tela de 10 polegadas, 128 GB e Wi-Fi.", "Estudo portátil"),
    (9, "SSD Sprint 1 TB", "Acessórios", 45990, "ssd", "Armazenamento externo de 1 TB com conexão USB-C.", "Espaço extra"),
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS produtos (
 id INTEGER PRIMARY KEY, nome TEXT NOT NULL, categoria TEXT NOT NULL,
 preco_centavos INTEGER NOT NULL CHECK(preco_centavos > 0),
 icone TEXT NOT NULL, descricao TEXT NOT NULL, destaque TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pedidos (
 id INTEGER PRIMARY KEY AUTOINCREMENT, criado_em TEXT NOT NULL,
 total_centavos INTEGER NOT NULL CHECK(total_centavos > 0)
);
CREATE TABLE IF NOT EXISTS itens_pedido (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 pedido_id INTEGER NOT NULL REFERENCES pedidos(id),
 produto_id INTEGER NOT NULL REFERENCES produtos(id),
 quantidade INTEGER NOT NULL CHECK(quantidade > 0),
 preco_unitario_centavos INTEGER NOT NULL CHECK(preco_unitario_centavos > 0)
);
CREATE INDEX IF NOT EXISTS idx_pedidos_data ON pedidos(criado_em);
CREATE INDEX IF NOT EXISTS idx_itens_pedido ON itens_pedido(pedido_id);
CREATE INDEX IF NOT EXISTS idx_itens_produto ON itens_pedido(produto_id);
"""


def agora():
    return datetime.now(timezone.utc)


def iso(data):
    return data.astimezone(timezone.utc).isoformat(timespec="seconds")


def conectar():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def registrar_pedido(itens, criado_em=None):
    """Registra uma venda simulada em uma transação, usando preços do banco."""
    if not isinstance(itens, list) or not 1 <= len(itens) <= 30:
        raise ValueError("Inclua entre 1 e 30 itens no pedido.")
    consolidados = {}
    for item in itens:
        if not isinstance(item, dict):
            raise ValueError("Item inválido.")
        produto_id, quantidade = item.get("produto_id"), item.get("quantidade")
        if type(produto_id) is not int or type(quantidade) is not int or not 1 <= quantidade <= 20:
            raise ValueError("Use um produto válido e quantidade de 1 a 20.")
        consolidados[produto_id] = consolidados.get(produto_id, 0) + quantidade
        if consolidados[produto_id] > 20:
            raise ValueError("O limite é 20 unidades por produto.")
    with conectar() as conn:
        linhas, total = [], 0
        for produto_id, quantidade in consolidados.items():
            produto = conn.execute("SELECT * FROM produtos WHERE id=?", (produto_id,)).fetchone()
            if not produto:
                raise ValueError("Produto não encontrado.")
            preco = produto["preco_centavos"]
            total += preco * quantidade
            linhas.append((produto_id, quantidade, preco))
        cursor = conn.execute("INSERT INTO pedidos(criado_em,total_centavos) VALUES (?,?)", (iso(criado_em or agora()), total))
        pedido_id = cursor.lastrowid
        conn.executemany("INSERT INTO itens_pedido(pedido_id,produto_id,quantidade,preco_unitario_centavos) VALUES (?,?,?,?)", [(pedido_id, *linha) for linha in linhas])
    return {"pedido_id": pedido_id, "total_centavos": total, "ficticio": True}


def inicializar():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with conectar() as conn:
        conn.executescript(SCHEMA)
        conn.executemany("INSERT OR IGNORE INTO produtos VALUES (?,?,?,?,?,?,?)", PRODUTOS)
        tem_pedidos = conn.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
    if not tem_pedidos:
        rng, referencia = random.Random(42), agora()
        for n in range(60):
            # As primeiras 20 vendas estão dentro das últimas 24 horas.
            horas = 0.5 + n if n < 20 else 25 + (n - 20) * 3.5
            ids = rng.choices(range(1, 10), weights=[2, 12, 3, 7, 10, 5, 3, 2, 6], k=rng.randint(1, 3))
            itens = [{"produto_id": pid, "quantidade": 1 + (n % 2)} for pid in sorted(set(ids))]
            registrar_pedido(itens, referencia - timedelta(hours=horas))


def gerar_vendas(quantidade=5):
    rng = random.Random()
    return [registrar_pedido([{"produto_id": rng.choices(range(1, 10), weights=[2, 12, 3, 7, 10, 5, 3, 2, 6])[0], "quantidade": rng.randint(1, 3)}]) for _ in range(quantidade)]


def atualizar_datas():
    """Move o histórico inteiro para perto de agora, mantendo os intervalos."""
    with conectar() as conn:
        ultimo = conn.execute("SELECT MAX(criado_em) FROM pedidos").fetchone()[0]
        if not ultimo:
            return
        deslocamento = agora() - timedelta(minutes=30) - datetime.fromisoformat(ultimo)
        linhas = conn.execute("SELECT id,criado_em FROM pedidos").fetchall()
        conn.executemany("UPDATE pedidos SET criado_em=? WHERE id=?", [(iso(datetime.fromisoformat(linha["criado_em"]) + deslocamento), linha["id"]) for linha in linhas])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Prepara a base fictícia da loja.")
    parser.add_argument("--atualizar-datas", action="store_true", help="Reaproxima as datas do histórico de hoje.")
    args = parser.parse_args()
    inicializar()
    if args.atualizar_datas:
        atualizar_datas()
    print(f"Banco pronto: {DB_PATH}")
