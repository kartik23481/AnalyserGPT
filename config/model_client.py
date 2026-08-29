import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constant import MODEL

load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')


def get_model_client():
    MODEL_CLIENT = OpenAIChatCompletionClient(
        model=MODEL,
        api_key=API_KEY,
    )
    return MODEL_CLIENT