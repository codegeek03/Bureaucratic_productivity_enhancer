import unittest
import os
import logging
from main import main

class TestLocalRAGAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.DEBUG)
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

    def setUp(self):
        self.test_pdf_path = "test_document.pdf"
        # Create a test PDF file here if needed
        
    def test_initialization(self):
        result = main(
            user_query="",
            initialize=True,
            pdf_path=self.test_pdf_path,
            dry_run=True
        )
        self.assertEqual(result, "PDF processed and ready for questions!")

    def test_query_without_initialization(self):
        result = main(
            user_query="What is in the document?",
            initialize=False,
            pdf_path=None,
            dry_run=True
        )
        self.assertTrue("Error: Vector store not initialized" in result)

    def tearDown(self):
        if os.path.exists("./chroma_db"):
            import shutil
            shutil.rmtree("./chroma_db")

def run_manual_test():
    logging.basicConfig(level=logging.DEBUG)
    
    test_pdf_path = "path/to/your/test.pdf"  # Replace with actual PDF path
    test_query = "What is the main topic of this document?"

    print("Starting Local RAG Agent Test...")
    
    print("\n1. Initializing with PDF...")
    result = main(
        user_query="",
        initialize=True,
        pdf_path=test_pdf_path,
        dry_run=False
    )
    print(f"Initialization result: {result}")

    print("\n2. Testing query...")
    response = main(
        user_query=test_query,
        initialize=False,
        pdf_path=None,
        dry_run=False
    )
    print(f"Query response: {response}")

if __name__ == "__main__":
    choice = input("Run unit tests? (y/n): ").lower()
    if choice == 'y':
        unittest.main(argv=['first-arg-is-ignored'])
    else:
        run_manual_test()