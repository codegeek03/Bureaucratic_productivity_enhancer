import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

import hashlib

from gptcache import Cache
from langchain.globals import set_llm_cache
from gptcache.manager.factory import manager_factory
from gptcache.processor.pre import get_prompt
from langchain_community.cache import GPTCache


def get_hashed_name(name):
    return hashlib.sha256(name.encode()).hexdigest()


def init_gptcache(cache_obj: Cache, llm: str):
    hashed_llm = get_hashed_name(llm)
    cache_obj.init(
        pre_embedding_func=get_prompt,
        data_manager=manager_factory(manager="map", data_dir=f"map_cache_{hashed_llm}"),
    )


set_llm_cache(GPTCache(init_gptcache))

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
