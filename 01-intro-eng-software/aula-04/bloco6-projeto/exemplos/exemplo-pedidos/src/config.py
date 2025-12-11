from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Sistema de Pedidos"
    app_version: str = "1.0.0"

settings = Settings()
