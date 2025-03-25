from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import Document
from langchain.schema.retriever import BaseRetriever
from typing import List, Any
from supabase import create_client, Client
from pydantic import BaseModel, Field
from fastapi import HTTPException
import tempfile
import os

# Define a proper Pydantic model for the retriever
class SupabaseRetriever(BaseRetriever, BaseModel):
    supabase_client: Client = Field(..., description="Supabase client instance")
    embeddings: Any = Field(..., description="Embeddings model instance")

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str) -> List[Document]:
        query_embedding = self.embeddings.embed_query(query)
        
        result = self.supabase_client.rpc(
            'match_documents',
            {'query_embedding': query_embedding, 'match_count': 5}
        ).execute()
        
        docs = []
        for item in result.data:
            docs.append(Document(
                page_content=item['content'],
                metadata=item['metadata']
            ))
        return docs

    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        return self._get_relevant_documents(query)

class RAGService:
    def __init__(self, google_api_key: str, supabase_url: str, supabase_service_key: str):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=google_api_key
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
                try:
                    # Clean the text content
                    content = doc.page_content.replace('\x00', '')
                    cleaned_content = ''.join(char for char in content if ord(char) < 128)
                    
                    vector = self.embeddings.embed_query(cleaned_content)
                    
                    data = {
                        'content': cleaned_content,
                        'metadata': {'page': doc.metadata.get('page', 0)},
                        'embedding': vector
                    }
                    
                    self.supabase.table('documents').insert(data).execute()
                except Exception as e:
                    print(f"Error processing chunk: {str(e)}")
                    continue

            # Initialize the chat chain with Gemini
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-002",
                google_api_key=self.google_api_key,
                temperature=0.7
            )
            
            # Create retriever instance with proper model initialization
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
        except Exception as e:
            print(f"Error in process_pdf: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            os.unlink(tmp_path)

    async def get_response(self, question: str) -> str:
        if not self.chat_chain:
            raise ValueError("No documents have been processed yet")
        
        response = await self.chat_chain.ainvoke({
            "question": question,
            "chat_history": []
        })
        return response["answer"]