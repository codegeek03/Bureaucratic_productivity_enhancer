from langchain_groq import ChatGroq
import hashlib
from gptcache import Cache
from langchain.globals import set_llm_cache
from gptcache.manager.factory import manager_factory
from gptcache.processor.pre import get_prompt
from langchain_community.cache import GPTCache
from dotenv import load_dotenv

load_dotenv()

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
        Creates a professional, grammatically correct template for generating responses.
        
        Returns:
            str: A string containing the enhanced response template.
        """
        template = """
        You are a professional assistant. Your goal is to provide grammatically correct, polished, and professional responses.

        Task:
        1. Review the question and correct any grammatical mistakes.
        2. Enhance the professionalism of the query by rephrasing it in a formal tone.
        3. Provide a clear, concise, and to-the-point response that is a corrected version of the query text. Do not include any reasoning or extra texts.

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
        print("Generating response for query:", query)
        messages = [
            ("system", "You are a grammar correction and professionalism enhancement assistant. Your goal is to provide grammatically correct, professional, and clear responses. The response should be to the point and a corrected version of the query text. Do not include any reasoning or extra texts."),
            ("human", self.prompt.format(question=query))
        ]
        
        ai_msg = self.llm.invoke(messages)
        return ai_msg.content

if __name__ == "__main__":
    question = "can you explain how langchain works and its applications?"
    generator = ProfessionalResponseGenerator()
    response = generator.generate_response(question)
    print("Professional Response:", response)