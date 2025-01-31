from langchain_groq import ChatGroq

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

class ProfessionalResponseGenerator:
    def __init__(self, model_name="mixtral-8x7b-32768"):
        """
        Initializes the ProfessionalResponseGenerator with the given language model.
        
        Args:
            model_name (str): The name of the model to be used for generating responses. Default is "mixtral-8x7b-32768".
        """
        self.model_name = model_name
        self.llm = ChatGroq(
            model=self.model_name,
            temperature=0,  
            max_tokens=None,  
            timeout=None,  
            max_retries=2,  
        )
        self.prompt = self.create_professional_template()

    def create_professional_template(self):
        """
        Creates a professional, grammatically correct template for generating responses with Chain-of-Thought (COT) reasoning.
        
        Returns:
            str: A string containing the enhanced response template.
        """
        template = """
        You are a professional assistant with the goal of providing grammatically correct, polished, and professional responses.

        Task:
        1. Review the question and correct any grammatical mistakes.
        2. Enhance the professionalism of the query by rephrasing it in a formal tone.
        3. Use Chain-of-Thought reasoning to break down the question logically. 
        4. Give only bulleted and important points, nothing more than that. I need only to-the-point responses.

        Question: {question}

        Response: 
        """
        return template

    def generate_response(self, query):
        """
        Generates a professional response for the given query using the language model.
        
        Args:
            query (str): The question for which the response is to be generated.
        
        Returns:
            str: The professionally generated response.
        """
        messages = [
            ("system", "You are a helpful assistant. Your goal is to provide grammatically correct, professional, and clear responses."),
            ("human", self.prompt.format(question=query))
        ]
        
        ai_msg = self.llm.invoke(messages)
        return ai_msg.content

if __name__ == "__main__":
    question = "can you explain how langchain works and its applications?"
    generator = ProfessionalResponseGenerator()
    response = generator.generate_response(question)
    print("Professional Response:", response)
