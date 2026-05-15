from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): 
    PROJECT_NAME: str = 'Payment Service'
    DATABASE_URL:  str
    ORDER_SERVICE_URL: str
    PORT: int
        
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    
    
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISH_KEY: str
    
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()