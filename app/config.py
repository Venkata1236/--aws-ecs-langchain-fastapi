import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
APP_TITLE = os.getenv("APP_TITLE", "LangChain AI API")