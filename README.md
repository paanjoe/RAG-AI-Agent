# RAG AI Application

A Retrieval-Augmented Generation (RAG) application that enables users to chat with their PDF documents using Google's Gemini AI model.

This is for my personal experiment use only & educational purposes.

## Features

- PDF document upload and processing
- Vector embeddings generation using Gemini API
- Similarity search using pgvector
- Conversational AI with context from uploaded documents
- Dark/Light mode support
- User-provided API key management

## Tech Stack

### Frontend

- Next.js 14
- React
- Flowbite UI Components
- TailwindCSS

### Backend

- FastAPI
- LangChain
- Google Gemini API
- PyPDF

### Database

- Supabase
- PostgreSQL with pgvector extension

## Technical Architecture

```mermaid
graph TB
    subgraph Frontend["Frontend (Next.js)"]
        UI[User Interface]
        Upload[PDF Upload Component]
        Chat[Chat Component]
        Theme[Theme Provider]
    end

    subgraph Backend["Backend (FastAPI)"]
        API[FastAPI Endpoints]
        RAG[RAG Service]
        PDF[PDF Processor]
        LLM[Gemini LLM]
    end

    subgraph Database["Vector Database (Supabase)"]
        PG[PostgreSQL]
        Vector[pgvector]
        Embed[Embeddings Storage]
    end

    %% User Flow
    User((User)) -->|1. Uploads PDF| Upload
    Upload -->|2. Send PDF| API
    API -->|3. Process| PDF
    PDF -->|4. Generate Embeddings| RAG
    RAG -->|5. Store Vectors| Vector

    %% Chat Flow
    User -->|6. Ask Question| Chat
    Chat -->|7. Query| API
    API -->|8. Get Context| RAG
    RAG -->|9. Search Similar| Vector
    Vector -->|10. Return Context| RAG
    RAG -->|11. Generate Answer| LLM
    LLM -->|12. Response| API
    API -->|13. Display Answer| Chat

    %% Styling
    classDef frontend fill:#47B4B6,stroke:#333,stroke-width:2px;
    classDef backend fill:#FF9776,stroke:#333,stroke-width:2px;
    classDef database fill:#7C3AED,stroke:#333,stroke-width:2px;
    classDef user fill:#4CAF50,stroke:#333,stroke-width:2px;

    class UI,Upload,Chat,Theme frontend;
    class API,RAG,PDF,LLM backend;
    class PG,Vector,Embed database;
    class User user;
```

## Flow Description

1. **PDF Upload Flow**

   - User uploads a PDF document
   - Frontend sends the file to Backend
   - Backend processes PDF into chunks
   - Gemini API generates embeddings
   - Vectors are stored in Supabase pgvector

2. **Chat Flow**
   - User sends a question
   - Backend searches for relevant context
   - Similar vectors are retrieved
   - Gemini API generates response
   - Answer is displayed to user

## System Components

### Frontend Components

- **PDF Upload**: Handles document upload
- **Chat Interface**: Manages conversation
- **Theme Provider**: Controls dark/light mode
- **API Key Management**: Secures user credentials

### Backend Services

- **FastAPI Endpoints**: REST API interface
- **RAG Service**: Core retrieval-augmented generation
- **PDF Processor**: Document chunking and processing
- **LLM Integration**: Gemini API communication

### Database Structure

- **PostgreSQL**: Base database system
- **pgvector**: Vector similarity search
- **Embeddings**: Document vector storage

## Security Considerations

- User API keys stored locally
- Secure communication over HTTPS
- No permanent storage of uploaded documents
