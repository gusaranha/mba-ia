from openai import OpenAI

class VLLM:

    def __init__(self, vllm_host, vllm_model, api_key):
        self.cliente = None
        self.cliente = self._get_cliente_openai(vllm_host, api_key)
        self.models = []
        for model_data in self.cliente.models.list().model_dump()['data']:
            if model_data['object'] == 'model':
                self.models.append(model_data['id'])

        model = None
        if self.models and vllm_model not in self.models: 
            print(f"Modelo {vllm_model} nao encontrado em {vllm_host}.")
            print(f"<< servidor VLLM usando {model} >>")
            model = self.models[0]
            self.vllm_model = model
        else:
            print(f"<< servidor VLLM usando {vllm_model} >>")
            self.vllm_model = vllm_model


    def _get_cliente_openai(self, host='localhost:11434', api_key=None):
        if api_key is None:
            if 'localhost' in host or '127.0.0.1'in host or '0.0.0.0' in host:
                api_key = "ollama"
            else:
                api_key = "EMPTY"
                
        cliente_openai = OpenAI(
            base_url=f"http://{host}/v1",
            api_key=api_key,
        )
        return cliente_openai


    def get_resposta(self, img_base64, pergunta, answer_json=False):
        messages = []
        if answer_json:
            messages = [
                {
                    "role": "system",
                    "content": "Você é um extrator de dados JSON. Responda apenas com o objeto JSON solicitado, sem markdown ou explicações."
                },
            ]

        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": pergunta},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        },
                    },
                ],
            })

        response = self.cliente.chat.completions.create(
            model=self.vllm_model,
            messages=messages,
        )

        return response.choices[0].message.content