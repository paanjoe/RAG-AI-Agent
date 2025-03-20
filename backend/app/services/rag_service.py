from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
import tempfile
import os

class RAGService:
    def __init__(self, google_api_key: str):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=google_api_key
        )
        self.vector_store = None
        self.chat_chain = None
        self.google_api_key = google_api_key

    async def process_pdf(self, file: bytes):
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file)
            tmp_path = tmp_file.name

        try:
            # Load and split the PDF
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(documents)

            # Create vector store
            self.vector_store = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings
            )

            # Initialize the chat chain with Gemini
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-002",
                google_api_key=self.google_api_key,
                temperature=0.7
            )
            self.chat_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vector_store.as_retriever()
            )

            return {"message": "PDF processed successfully"}
        finally:
            # Clean up the temporary file
            os.unlink(tmp_path)

    async def get_response(self, question: str, chat_history: list = []):
        if not self.chat_chain:
            raise ValueError("No documents have been processed yet")
        
        response = await self.chat_chain.ainvoke({
            "question": question,
            "chat_history": chat_history
        })
        return response["answer"]