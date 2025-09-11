from google import genai
from dotenv import load_dotenv
import os
from google.genai import types


class GemmaAPI:
    def __init__(self):
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_TOKEN"))
        self.conversation = []

    def BuildModelDetails(self, purpose=None):
        purpose = (
            purpose or
            "You are a helpful assistant that analyzes errors in code and suggests fixes."
        )
        system_msg = types.Content(
            role="user",
            parts=[types.Part(text=purpose)]
        )
        self.conversation.append(system_msg)
        return system_msg

    def ConstructModel(self, filepath=None,
                       askedPrompt="Look at this error and explain how a fix can be written"):
        if not any(c.role == "user" for c in self.conversation):
            self.BuildModelDetails()

        if filepath:
            uploaded_file = self.client.files.upload(filepath)
            content = types.Content(
                role="user",
                parts=[
                    types.Part(text=askedPrompt),
                    uploaded_file
                ]
            )
        else:
            content = types.Content(
                role="user",
                parts=[types.Part(text=askedPrompt)]
            )

        self.conversation.append(content)

        response = self.client.models.generate_content(
            model="gemma-3-27b-it",
            contents=self.conversation
        )

        formatted_response = types.Content(
            role="model",
            parts=[types.Part(text=response.text)]
        )
        self.conversation.append(formatted_response)

        return response.text

    def SendMessage(self, text,askedPrompt = "Look at this error and explain how a fix can be written"):

        if not any(c.role == "system" for c in self.conversation):
            self.BuildModelDetails()

        content = types.Content(
                role='user',
                parts=[ 
                       types.Part(text=f"Task : {askedPrompt}"),
                       types.Part(text=f"Error :\n{text}")
                       ]
                )
        self.conversation.append(content)

        response = self.client.models.generate_content(
            model="gemma-3-27b-it",
            contents=self.conversation
        )

        formatted_response = types.Content(
            role="model",
            parts=[types.Part(text=response.text)]
        )
        self.conversation.append(formatted_response)

        return response.text

API = GemmaAPI()
response = API.SendMessage("IndexError:index out of bound")
print(response)

