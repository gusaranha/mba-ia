"""Loja pronta para a aula. Execute: python app.py"""
import secrets
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, render_template, request, session
from banco import inicializar, registrar_pedido, gerar_vendas
from consultas import listar_produtos, produtos_mais_vendidos, valor_medio, vendas_ultimas_24h

LOGS = Path(__file__).resolve().parent / "logs"
MESES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
trava_log = threading.Lock()


def aspas(valor):
    """Escapa aspas e barras como o Apache faz nos campos entre aspas."""
    return (valor or "-").replace("\\", "\\\\").replace('"', '\\"')


def registrar_acesso(resposta):
    """Grava a requisição no formato Apache Combined em logs/log_AAAA-MM-DD.log."""
    agora = datetime.now().astimezone()
    data = f"{agora:%d}/{MESES[agora.month - 1]}/{agora:%Y:%H:%M:%S %z}"
    caminho = request.path + ("?" + request.query_string.decode("latin-1") if request.query_string else "")
    requisicao = f"{request.method} {caminho} {request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1')}"
    tamanho = resposta.content_length or "-"
    linha = (f'{request.remote_addr or "-"} - - [{data}] "{aspas(requisicao)}" {resposta.status_code} {tamanho} '
             f'"{aspas(request.referrer)}" "{aspas(request.user_agent.string)}"\n')
    LOGS.mkdir(exist_ok=True)
    with trava_log, open(LOGS / f"log_{agora:%Y-%m-%d}.log", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)
    return resposta


def create_app():
    inicializar()
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)
    app.config["MAX_CONTENT_LENGTH"] = 32 * 1024
    app.after_request(registrar_acesso)

    @app.before_request
    def token_local():
        session.setdefault("token", secrets.token_hex(24))
        if request.method == "POST" and request.headers.get("X-Lab-Token") != session["token"]:
            return jsonify(erro="Recarregue a página antes de registrar a venda."), 403

    @app.get("/")
    def catalogo():
        return render_template("index.html", produtos=listar_produtos(), token=session["token"])

    @app.get("/painel")
    def painel():
        return render_template("painel.html", token=session["token"])

    @app.get("/api/produtos")
    def api_produtos():
        return jsonify(produtos=listar_produtos(request.args.get("categoria")))

    @app.get("/api/metricas")
    def api_metricas():
        return jsonify(vendas=vendas_ultimas_24h(), medias=valor_medio(), ranking=produtos_mais_vendidos())

    @app.post("/api/pedidos")
    def api_pedido():
        dados = request.get_json(silent=True)
        try:
            if not isinstance(dados, dict):
                raise ValueError("Pedido inválido.")
            resultado = registrar_pedido(dados.get("itens"))
        except ValueError as exc:
            return jsonify(erro=str(exc)), 400
        return jsonify(resultado), 201

    @app.post("/api/simular-vendas")
    def api_simular():
        return jsonify(pedidos=gerar_vendas(5), mensagem="Cinco vendas fictícias registradas."), 201

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
