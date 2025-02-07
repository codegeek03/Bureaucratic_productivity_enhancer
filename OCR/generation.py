import base64
import os
from dotenv import load_dotenv
from mistralai import Mistral
import re

load_dotenv()

def clean_text(text):
        text = re.sub(r"\s+", " ", text)  
        text = re.sub(r"[^a-zA-Z0-9\s.,!?%$]", "", text) 
        text = text.strip()
        return text

class ImageAnalyzer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.model = "pixtral-12b-2409"
        self.client = Mistral(api_key=self.api_key)
        self.base64_image = self._encode_image()
        
    

    def _encode_image(self):
        try:
            with open(self.image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"Error: The file {self.image_path} was not found.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def analyze_image(self):
        if not self.base64_image:
            return "Failed to encode image."

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all visible text from this image and provide a detailed description of its contents, including objects, landmarks, and any relevant contextual details."
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{self.base64_image}"
                    }
                ]
            }
        ]

        chat_response = self.client.chat.complete(
            model=self.model,
            messages=messages
        )

        return clean_text(chat_response.choices[0].message.content)


if __name__ == "__main__":
    image_path = "receipt_image2.jpg"
    analyzer = ImageAnalyzer(image_path)
    result = analyzer.analyze_image()
    print(result)

