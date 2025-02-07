from langchain_groq import ChatGroq
import hashlib
from gptcache import Cache
from langchain.globals import set_llm_cache
from gptcache.manager.factory import manager_factory
from gptcache.processor.pre import get_prompt
from langchain_community.cache import GPTCache
from dotenv import load_dotenv
import requests
import json
import logging
from typing import Dict, Tuple

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_hashed_name(name):
    return hashlib.sha256(name.encode()).hexdigest()

def init_gptcache(cache_obj: Cache, llm: str):
    hashed_llm = get_hashed_name(llm)
    cache_obj.init(
        pre_embedding_func=get_prompt,
        data_manager=manager_factory(manager="map", data_dir=f"map_cache_{hashed_llm}"),
    )

set_llm_cache(GPTCache(init_gptcache))

class FactChecker:
    def __init__(self):
        self.wiki_api = "https://en.wikipedia.org/w/api.php"
        self.news_api = "https://newsapi.org/v2/everything"  # You'll need an API key
    
    def verify_fact(self, statement: str) -> Tuple[bool, str]:
        """
        Verifies a factual statement using Wikipedia and news sources.
        
        Args:
            statement (str): The statement to verify
            
        Returns:
            Tuple[bool, str]: (is_verified, explanation)
        """
        try:
            # Search Wikipedia
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": statement,
                "srprop": "snippet"
            }
            
            response = requests.get(self.wiki_api, params=params)
            data = response.json()
            
            if data["query"]["search"]:
                return True, "Fact verified through Wikipedia"
            
            return False, "Unable to verify fact - please verify independently"
            
        except Exception as e:
            logger.error(f"Error in fact verification: {str(e)}")
            return False, "Error in fact verification process"

class ProfessionalResponseGenerator:
    def __init__(self, model_name="mixtral-8x7b-32768"):
        """
        Initializes the ProfessionalResponseGenerator with enhanced fact-checking capabilities.
        
        Args:
            model_name (str): The name of the model to be used. Default is "mixtral-8x7b-32768".
        """
        self.model_name = model_name
        self.llm = ChatGroq(
            model=self.model_name,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        self.fact_checker = FactChecker()
        self.prompt_templates = self.create_prompt_templates()

    def create_prompt_templates(self) -> Dict[str, str]:
        """
        Creates a dictionary of specialized prompts for different types of content.
        
        Returns:
            Dict[str, str]: Dictionary containing different prompt templates
        """
        return {
            "grammar_correction": """
                Correct the following text for grammar and clarity.
                Focus on:
                - Grammar and punctuation
                - Professional tone
                - Clarity and conciseness
                
                Text: {text}
                
                Provide only the corrected text without explanations.
            """,
            
            "fact_check": """
                Analyze the following statement for factual claims:
                
                Statement: {text}
                
                Identify key factual claims and assess their verifiability.
                Format response as:
                CLAIMS: [List key factual claims]
                VERIFICATION_STATUS: [True/False/Uncertain]
                CORRECTED_STATEMENT: [If needed, provide corrected version]
            """
        }

    def process_statement(self, text: str) -> Dict:
        """
        Processes a statement through grammar correction and fact checking.
        
        Args:
            text (str): The input text to process
            
        Returns:
            Dict: Processing results including corrections and fact-check results
        """
        try:
            # Step 1: Grammar Correction
            messages = [
                ("system", "You are a precise grammar correction assistant. Provide only the corrected text without explanations."),
                ("human", self.prompt_templates["grammar_correction"].format(text=text))
            ]
            corrected_text = self.llm.invoke(messages).content

            # Step 2: Fact Checking
            messages = [
                ("system", "You are a fact-checking assistant. Identify and verify factual claims."),
                ("human", self.prompt_templates["fact_check"].format(text=corrected_text))
            ]
            fact_check_response = self.llm.invoke(messages).content

            # Step 3: Verify key facts
            is_verified, verification_note = self.fact_checker.verify_fact(corrected_text)

            return {
                "original_text": text,
                "corrected_text": corrected_text,
                "fact_check_results": {
                    "is_verified": is_verified,
                    "verification_note": verification_note,
                    "detailed_analysis": fact_check_response
                },
                "alert_level": "HIGH" if not is_verified else "LOW"
            }

        except Exception as e:
            logger.error(f"Error in processing statement: {str(e)}")
            return {
                "error": str(e),
                "original_text": text,
                "corrected_text": text,
                "fact_check_results": {
                    "is_verified": False,
                    "verification_note": "Error in processing",
                    "detailed_analysis": "Unable to complete analysis"
                },
                "alert_level": "ERROR"
            }

    def generate_response(self, query: str) -> str:
        """
        Generates a professional response with fact-checking and alerts.
        
        Args:
            query (str): The input query to process
            
        Returns:
            str: JSON string containing the processed response
        """
        logger.info(f"Processing query: {query}")
        
        result = self.process_statement(query)
        
        # Format the response as a structured output
        response = {
            "original_text": result["original_text"],
            "corrected_version": result["corrected_text"],
            "fact_check": {
                "alert_level": result["alert_level"],
                "verification_status": result["fact_check_results"]["is_verified"],
                "verification_note": result["fact_check_results"]["verification_note"]
            },
            "detailed_analysis": result["fact_check_results"]["detailed_analysis"]
        }
        
        return response

if __name__ == "__main__":
    # Test the enhanced version
    test_statements = [
        "the earth is flat and gravity doesnt exist",
        "Python was created by Guido van Rossum in 1991",
        "artificial intelligence was invented last year"
    ]
    
    generator = ProfessionalResponseGenerator()
    
    for statement in test_statements:
        print("\nTesting statement:", statement)
        response = generator.generate_response(statement)
        print("Response:", response)
        print("-" * 80)