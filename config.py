import os

from dotenv import load_dotenv

APP_NAME = "DevMentor"

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("MODEL_NAME")