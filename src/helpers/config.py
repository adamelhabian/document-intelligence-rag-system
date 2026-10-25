from pydantic_settings import BaseSettings, SettingsConfigDict


# BaseSettings is a class that reads configuration values from environment variables and 
# can load them from a .env file when configured to do so. 
# we can say basesettings load and validate the configrations

class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENAI_API_KEY:str
    FILE_DEFAULT_CHUNK_SIZE:int
    
    FILE_ALLOWED_EXTENSIONS: list[str] = ["text/plain", "application/pdf"]
    FILE_MAX_SIZE:int=10

    MONGODB_URL: str
    MONGODB_DATABASE :str


    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    # OPENAI_API_KEY: str = None
    # OPENAI_API_URL: str = None
    GEMINI_API_KEY: str = None
    COHERE_API_KEY: str = None

    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None
    INPUT_DAFAULT_MAX_CHARACTERS: int = None
    GENERATION_DAFAULT_MAX_TOKENS: int = None
    GENERATION_DAFAULT_TEMPERATURE: float = None
    

    #This tells Pydantic Settings to read configuration values from a file named .env
    class Config:
        env_file=".env"
        #Now, Pydantic can load these values instead of requiring you to hardcode them in Python.



def get_settings():
    return Settings()


# BaseSettings → Loads and validates configuration.
# Settings → Defines which configuration values your application needs.
# SettingsConfigDict → Configures how settings are loaded.
# .env → Stores configuration values outside your Python code.
# get_settings() → Creates and returns a settings object