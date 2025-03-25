from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import Document
from langchain.schema.retriever import BaseRetriever
from typing import List, Any, Tuple
from supabase import create_client, Client
from pydantic import BaseModel, Field
from fastapi import HTTPException
import tempfile
import os
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores.supabase import SupabaseVectorStore

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
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=google_api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        self.chat_history = []
        self.retriever = None
        self._initialize_retriever()

    def _initialize_retriever(self):
        try:
            # Create a retriever from Supabase
            self.retriever = SupabaseVectorStore(
                self.supabase,
                self.embeddings,
                table_name="documents",
                query_name="match_documents"
            ).as_retriever(search_kwargs={"k": 3})
        except Exception as e:
            print(f"Error initializing retriever: {str(e)}")
            raise

    async def chat(self, question: str) -> str:
        try:
            if not self.retriever:
                return "Please upload a document first."

            # Create conversation chain if it doesn't exist
            if not hasattr(self, 'conversation_chain'):
                memory = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True,
                    output_key="answer"
                )
                
                self.conversation_chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=self.retriever,
                    memory=memory,
                    return_source_documents=True,
                    verbose=True
                )

            # Get response from conversation chain
            response = await self.conversation_chain.ainvoke({
                "question": question,
                "chat_history": self.chat_history
            })

            # Update chat history with just the question and answer
            self.chat_history.append((question, response['answer']))

            return response['answer']

        except Exception as e:
            print(f"Error in chat: {str(e)}")
            raise

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

            # Clear existing documents using a proper WHERE clause
            self.supabase.table('documents').delete().neq('id', 0).execute()
            # Or alternatively:
            # self.supabase.table('documents').delete().execute(count='exact')

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

            # Reinitialize the retriever with new documents
            self._initialize_retriever()
            
            return {"message": "PDF processed successfully"}
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            raise
        finally:
            os.unlink(tmp_path)