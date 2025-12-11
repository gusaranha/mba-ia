from pydantic import BaseSettings

class Settings(BaseSettings):
    """Configurações da aplicação"""
    app_name: str = "Minha API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
