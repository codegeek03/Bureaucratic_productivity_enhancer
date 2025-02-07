from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from config import GROQ_API_KEY, GROQ_CHAT_MODEL

def create_qa_chain(vector_store):
    """Create QA chain using Groq"""
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model=GROQ_CHAT_MODEL,
        temperature=0.3
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    
    return qa_chain