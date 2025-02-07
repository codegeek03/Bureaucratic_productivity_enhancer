from vector_store import load_or_create_vector_store
from qa_chain import create_qa_chain
from pdf_loader import load_and_split_pdf
import os

def main():
    #pdf_path = "constitution_of_india.pdf"
    #print("Loading PDF...")
    #chunks = load_and_split_pdf(pdf_path)

    print("Loading vector store...")
    vector_store = load_or_create_vector_store()
    
    print("Setting up QA system...")
    qa_chain = create_qa_chain(vector_store)
    
    print("\nReady for questions!")
    
    # Interactive QA loop
    while True:
        question = input("\nEnter your question (or 'quit' to exit): ")
        
        if question.lower() == 'quit':
            break
            
        try:
            result = qa_chain.invoke({"query": question})
            print("\nAnswer:", result['result'])
            print("\nSources:")
            for doc in result['source_documents']:
                print(f"Page {doc.metadata['page']}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()