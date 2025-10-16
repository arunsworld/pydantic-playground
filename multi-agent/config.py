import os
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from typing import Union
from dotenv import load_dotenv
load_dotenv()

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "9010"))

MODEL_ID = os.getenv("MODEL_ID", "openai:gpt-4.1")
USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() == "true"

def get_model() -> Union[OpenAIChatModel, str]:
    if USE_OLLAMA:
        return OpenAIChatModel(
            model_name=MODEL_ID,
            provider=OllamaProvider(base_url='http://localhost:11434/v1'),  
        )
    return MODEL_ID