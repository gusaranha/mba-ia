class Entrada(BaseModel):
    texto: str
    cep: str | None = None

@app.post("/analisar")
def analisar(payload: Entrada):
    if payload.cep:
        cep_limpo = re.sub(r"\D", "", payload.cep)

        response = requests.get(
            f"https://viacep.com.br/ws/{cep_limpo}/json/",
            timeout=8
        )
        data = response.json()

        if data.get("erro"):
            return {"erro": "CEP não encontrado"}

        return {
            "texto": payload.texto,
            "cep": payload.cep,
            "localizacao": data
        }

    return {
        "texto": payload.texto,
        "localizacao": "não informada"
    }
