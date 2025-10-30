from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "PetSearch API"
    DATA_SOURCE: str = "local"

    MONGO_URI: str = "mongodb://localhost:27017/"
    MONGO_DB: str = "pet_database"
    COLLECTION: str = "pets"

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "pet_embeddings"

    EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"

    JWT_SECRET: str = "dev-secret"
    JWT_ALGORITHM: str = "HS256"

    CORS_ORIGINS: str = "http://127.0.0.1:5500,http://localhost:3000,http://127.0.0.1:3000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
