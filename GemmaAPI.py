from google import genai
from dotenv import load_env
import os

class GemmaAPI:
    def __init__(self):
        load_env()
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_TOKEN"))


    def 
