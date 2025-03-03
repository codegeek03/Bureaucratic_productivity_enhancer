import logging
from typing import List, Dict, Any
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

class LocalLLM:
    def __init__(self, model_name="TheBloke/Mistral-7B-Instruct-v0.2-GGUF"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"Using device: {self.device}")
        
        # Load model and tokenizer
        logging.info(f"Loading model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            load_in_8bit=True if self.device == "cuda" else False,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )
        
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
        )

    def generate_response(self, system_prompt: str, user_query: str) -> str:
        prompt = f"""### System: {system_prompt}

### User: {user_query}

### Assistant: """
        
        try:
            response = self.pipe(prompt)[0]['generated_text']
            # Extract only the assistant's response
            response = response.split("### Assistant:")[-1].strip()
            return response
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return ""

class LocalRAG:
    def __init__(self):
        self.llm = LocalLLM()
        
    def process_query(self, query: str, context: str) -> str:
        system_prompt = f"""You are a helpful assistant that answers questions based on the provided context. 
        If the context doesn't contain enough information to answer confidently, indicate that.
        
        Context:
        {context}
        """
        
        return self.llm.generate_response(system_prompt, query)
    
    def assess_confidence(self, response: str) -> bool:
        system_prompt = """Evaluate the confidence level of the following response.
        Consider:
        1. Completeness of the answer
        2. Specificity and precision
        3. Presence of uncertainty markers
        4. Consistency of information
        
        Respond with a confidence score between 0 and 1.
        """
        
        confidence_response = self.llm.generate_response(system_prompt, response)
        try:
            confidence_score = float(confidence_response.strip())
            return confidence_score > 0.7
        except:
            return False
    
    def synthesize_information(self, response: str) -> str:
        system_prompt = """Synthesize the information into a comprehensive response. 
        Use bullet points for lists and present the information in a clear, conversational tone.
        Highlight key findings at the beginning.
        """
        
        return self.llm.generate_response(system_prompt, response)