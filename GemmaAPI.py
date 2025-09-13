from google import genai
from dotenv import load_dotenv
import os
from google.genai import types
import shutil
class GemmaAPI:
    def __init__(self):
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_TOKEN"))
        self.conversation = []
        
    def convert_log_to_txt(self,log_path: str) -> str:
        if not os.path.exists(log_path):
            raise FileNotFoundError(f"{log_path} does not exist")

        base, _ = os.path.splitext(log_path)
        txt_path = base + ".txt"

        shutil.copyfile(log_path, txt_path)
        return txt_path


    def file_to_text(self, filepath: str) -> str:
        if not filepath:
            return None
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, "rb") as f:
            data = f.read()
        text = data.decode("utf-8", errors="ignore")
        return text
        

    def BuildModelDetails(self, purpose=None):
        purpose = purpose if purpose else "You are a helpful assistant that analyzes errors in code and suggests fixes."
        system_msg = types.Content(
            role="user",
            parts=[types.Part(text=purpose)]
        )
        self.conversation.append(system_msg)
        return system_msg
        

    def SendMessage(self, text,askedPrompt = "Look at this error and explain how a fix can be written", purpose=None, filepath=None):

        if not any(c.role == "system" for c in self.conversation):
            self.BuildModelDetails(purpose)

        file_txt  = self.file_to_text(filepath)
        if file_txt:
            askedPrompt += " I've attached file where error had happened"

            content = types.Content(
                    role='user',
                    parts=[ 
                           types.Part(text=f"Task : {askedPrompt}"),
                           types.Part(text=f"Error :\n{text}"),
                            types.Part(text=f"File :\n{file_txt}")
                           ]
                    )
        else:
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
