from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import Document
from langchain.schema.retriever import BaseRetriever
from typing import List, Any
from supabase import create_client, Client
from pydantic import Field
import numpy as np
import tempfile
import os

class SupabaseRetriever(BaseRetriever):
    supabase_client: Client = Field(...)
    embeddings: Any = Field(...)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, supabase_client: Client, embeddings: Any, **kwargs):
        super().__init__(supabase_client=supabase_client, embeddings=embeddings, **kwargs)

    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        query_vector = self.embeddings.embed_query(query)
        
        # Perform similarity search
        result = self.supabase_client.rpc(
            'match_documents',
            {'query_embedding': query_vector, 'match_count': 5}
        ).execute()
        
        # Convert to Document objects
        docs = []
        for item in result.data:
            docs.append(Document(
                page_content=item['content'],
                metadata=item['metadata']
            ))
        return docs

    def _get_relevant_documents(self, query: str) -> List[Document]:
        query_vector = self.embeddings.embed_query(query)
        
        result = self.supabase_client.rpc(
            'match_documents',
            {'query_embedding': query_vector, 'match_count': 5}
        ).execute()
        
        docs = []
        for item in result.data:
            docs.append(Document(
                page_content=item['content'],
                metadata=item['metadata']
            ))
        return docs

class RAGService:
    def __init__(self, google_api_key: str, supabase_url: str, supabase_service_key: str):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=google_api_key,
        )
        self.supabase = create_client(supabase_url, supabase_service_key)
        self.google_api_key = google_api_key
        self.chat_chain = None

    async def process_pdf(self, file: bytes):
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

            # Create vectors and store them in Supabase
            for doc in splits:
                vector = self.embeddings.embed_query(doc.page_content)
                
                # Insert document and its embedding
                data = {
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'embedding': vector
                }
                self.supabase.table('documents').insert(data).execute()

            # Initialize the chat chain with Gemini
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-002",
                google_api_key=self.google_api_key,
                temperature=0.7
            )
            
            # Create retriever instance with proper initialization
            retriever = SupabaseRetriever(
                supabase_client=self.supabase,
                embeddings=self.embeddings
            )

            # Initialize the chat chain
            self.chat_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=retriever,
                return_source_documents=True
            )

            return {"message": "PDF processed successfully"}
        finally:
            os.unlink(tmp_path)

    async def get_response(self, question: str, chat_history: list = []):
        if not self.chat_chain:
            raise ValueError("No documents have been processed yet")
        
        response = await self.chat_chain.ainvoke({
            "question": question,
            "chat_history": chat_history
        })
        return response["answer"]