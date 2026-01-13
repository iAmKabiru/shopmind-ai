from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os 

load_dotenv()

class Settings(BaseSettings):
    openai_api_key: str = os.getenv('OPENAI_API_KEY')

settings = Settings()