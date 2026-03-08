import gradio as gr
import requests

# URL base da API FastAPI
API_URL = "http://localhost:8000"

def testar_endpoint():
    """Chama o endpoint /teste"""
    try:
        response = requests.get(f"{API_URL}/teste")
        response.raise_for_status()
        return response.json()["mensagem"]
    except requests.exceptions.ConnectionError:
        return "Erro: API não está rodando. Inicie o FastAPI primeiro!"
    except Exception as e:
        return f"Erro: {str(e)}"

def buscar_dados_imagem(img_path):
    """Chama o endpoint /dados/{img_path}"""
    if not img_path:
        return "Por favor, insira o nome da imagem"
    
    try:
        response = requests.get(f"{API_URL}/dados/{img_path}")
        response.raise_for_status()
        return response.json()["mensagem"]
    except requests.exceptions.ConnectionError:
        return "Erro: API não está rodando. Inicie o FastAPI primeiro!"
    except Exception as e:
        return f"Erro: {str(e)}"

# Criar a interface Gradio
with gr.Blocks(title="Cliente FastAPI", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Cliente FastAPI com Gradio")
    gr.Markdown("Interface para testar os endpoints da API FastAPI")
    
    with gr.Tab("Teste Simples"):
        gr.Markdown("### Endpoint: `GET /teste`")
        gr.Markdown("Clique no botão abaixo para testar o endpoint básico")
        
        btn_teste = gr.Button(" Testar Endpoint", variant="primary")
        output_teste = gr.Textbox(label="Resposta da API", lines=2)
        
        btn_teste.click(fn=testar_endpoint, outputs=output_teste)
    
    with gr.Tab("Buscar Dados de Imagem"):
        gr.Markdown("### Endpoint: `GET /dados/{img_path}`")
        gr.Markdown("Digite o nome/caminho da imagem para buscar seus dados")
        
        with gr.Row():
            input_img_path = gr.Textbox(
                label="Nome da Imagem",
                placeholder="Ex: foto.jpg ou imagens/teste.png",
                scale=3
            )
            btn_buscar = gr.Button(" Buscar Dados", variant="primary", scale=1)
        
        output_dados = gr.Textbox(label="Resposta da API", lines=2)
        
        # Exemplos
        gr.Examples(
            examples=[
                ["teste.jpg"],
                ["visao_computacional.png"],
                ["lenna.png"]
            ],
            inputs=input_img_path
        )
        
        btn_buscar.click(fn=buscar_dados_imagem, inputs=input_img_path, outputs=output_dados)
        input_img_path.submit(fn=buscar_dados_imagem, inputs=input_img_path, outputs=output_dados)
    
    with gr.Tab("ℹ️ Instruções"):
        gr.Markdown("""
        ## Como usar:
        
        1. **Inicie o servidor FastAPI primeiro:**
```bash
           uvicorn seu_script:app --reload
```
        
        2. **Execute esta interface Gradio:**
```bash
           python cliente_gradio.py
```
        
        3. **Use as abas acima para testar os endpoints**
        
        ---
        
        ### Endpoints disponíveis:
        
        - **GET /teste** - Retorna uma mensagem de teste simples
        - **GET /dados/{img_path}** - Retorna dados sobre uma imagem específica
        
        ---
        
        **Observação:** Certifique-se de que a API está rodando em `http://localhost:8000`
        """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)