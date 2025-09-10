from google import genai
from dotenv import load_env
import os
from google.genai import types
class GemmaAPI:
    def __init__(self):
        load_env()
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_TOKEN"))
        self.conversation = []



    def BuildModelDetails(self,askedPrompt, purpose=None):
        purpose = "You are a helpful assistant that analyzes error in code and suggests fixes" if not purpose else purpose
        history = [
        types.Content(
            role="system",
            parts=[types.Part.from_text(text=purpose)]),

        types.Content(
            role="user",
            parts=[types.Part.from_text(text=askedPrompt)]),
            ]
    return history
    def ConstructModel(filepath=None):

        history = self.BuildModelDetails("Look at this error and try to fix it", None)
        for i in history:
            self.conversation.append(i)

        file = client.file.upload(filepath) if filepath else None

        response = client.models.generate_content(
        model="gemma-3-27b-it", contents=[history, file])

        FormattedResponse = types.Content(

                )


