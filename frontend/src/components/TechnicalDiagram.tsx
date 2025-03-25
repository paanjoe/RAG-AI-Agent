'use client';

import { Modal } from 'flowbite-react';

interface TechnicalDiagramProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function TechnicalDiagram({
  isOpen,
  onClose,
}: TechnicalDiagramProps) {
  return (
    <Modal show={isOpen} onClose={onClose} size="6xl">
      <Modal.Header>Technical Diagram - RAG AI Application</Modal.Header>
      <Modal.Body>
        <div className="space-y-6">
          <div className="rounded-lg bg-white p-4 dark:bg-gray-800">
            <h3 className="mb-4 text-lg font-semibold">
              Application Architecture
            </h3>
            <div className="overflow-x-auto">
              <pre className="whitespace-pre-wrap rounded-lg bg-gray-50 p-4 text-sm dark:bg-gray-900">
                {`
Frontend (Next.js)                    Backend (FastAPI)                    Vector Database (Supabase)
+----------------+                   +----------------+                   +-------------------+
|                |                   |                |                   |                   |
|  User Interface|   1. Upload PDF   |   FastAPI      |   2. Process PDF |    Supabase      |
|  - PDF Upload  |------------------>|   Endpoint     |------------------>|    - pgvector     |
|  - Chat UI     |                   |   /upload      |                   |    - Embeddings   |
|                |                   |                |                   |                   |
|                |   3. Chat Query   |                |   4. Search      |                   |
|                |------------------>|   /chat        |------------------>|                   |
|                |                   |                |                   |                   |
|                |   6. Response     |                |   5. Retrieve    |                   |
|                |<------------------|                |<------------------|                   |
+----------------+                   +----------------+                   +-------------------+
        |                                    |                                    |
        |                                    |                                    |
        v                                    v                                    v
+----------------+                   +----------------+                   +-------------------+
|  Technologies  |                   |  Technologies  |                   |   Technologies    |
|  - Next.js 14  |                   |  - FastAPI    |                   |   - PostgreSQL    |
|  - React       |                   |  - LangChain  |                   |   - pgvector      |
|  - Flowbite    |                   |  - Gemini API |                   |   - Supabase      |
|  - TailwindCSS |                   |  - PyPDF      |                   |                   |
+----------------+                   +----------------+                   +-------------------+

Flow:
1. User uploads PDF document through the frontend
2. Backend processes PDF, splits into chunks, and generates embeddings using Gemini API
3. Embeddings are stored in Supabase's pgvector database
4. User sends a question through the chat interface
5. Backend retrieves relevant document chunks using similarity search
6. Gemini API generates a response based on the retrieved context
7. Response is sent back to the user
                `}
              </pre>
            </div>
          </div>

          <div className="rounded-lg bg-white p-4 dark:bg-gray-800">
            <h3 className="mb-4 text-lg font-semibold">Key Features</h3>
            <ul className="list-inside list-disc space-y-2 text-sm">
              <li>PDF document processing and chunking</li>
              <li>Vector embeddings generation using Gemini API</li>
              <li>Similarity search using pgvector</li>
              <li>Conversational AI with context from uploaded documents</li>
              <li>Dark/Light mode support</li>
              <li>User-provided API key management</li>
            </ul>
          </div>
        </div>
      </Modal.Body>
    </Modal>
  );
}
