import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


class SpeechToText:
    def __init__(self, model_id="whisper-large-v3"):
        self.client = Groq()
        self.model_id = model_id
    
    def transcribe(self, audio_path, prompt=None, temperature=0.0, response_format="json"):
        """Transcribes audio file to text using Groq API."""
        with open(audio_path, "rb") as file:
            translation = self.client.audio.translations.create(
                file=(audio_path, file.read()),  
                model=self.model_id,  
                prompt=prompt,  
                response_format=response_format,  
                temperature=temperature  
            )
            return translation.text

if __name__ == "__main__":
    filename = "sample.m4a"
    
    stt = SpeechToText()
    
    transcript = stt.transcribe(filename)
    
    print("Transcription:", transcript)
