from pydantic_settings import BaseSettings
 
 
class Settings(BaseSettings):
    app_name: str = "OpsBrain"
    environment: str = "development"
    database_url: str = ""
    neo4j_uri: str = ""
    neo4j_user: str = ""
    neo4j_password: str = ""
    vector_db_api_key: str = ""
    llm_api_key: str = ""
 
    class Config:
        env_file = ".env"
 
 
settings = Settings()
