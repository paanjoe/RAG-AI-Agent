from typing import Optional
from app.services.rag_service import RAGService

class AppState:
    _instance = None
    rag_service: Optional[RAGService] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_rag_service(self, rag_service: RAGService):
        self.rag_service = rag_service

    def get_rag_service(self) -> Optional[RAGService]:
        return self.rag_service 