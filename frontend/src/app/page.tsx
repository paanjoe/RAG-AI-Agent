'use client';

import { useState } from 'react';

import ApiKeyInput from '@/components/ApiKeyInput';
import Chat from '@/components/Chat';
import FileUpload from '@/components/FileUpload';
import Footer from '@/components/Footer';
import NavBar from '@/components/NavBar';

export default function Home() {
  const [hasApiKey, setHasApiKey] = useState<boolean>(false);

  const handleApiKeyChange = (apiKey: string | null) => {
    setHasApiKey(!!apiKey);
  };

  return (
    <>
      <NavBar />
      <main className="container mx-auto max-w-4xl p-4">
        <h1 className="mb-8 text-center text-2xl font-bold">
          Experimenting RAG AI
        </h1>
        <div
          className="mb-4 rounded-lg bg-blue-50 p-4 text-sm text-blue-800 dark:bg-gray-800 dark:text-blue-400"
          role="alert"
        >
          <span className="font-medium">Information:</span> This site is only
          for my personal experiment on{' '}
          <b>Retrieval-Augmented Generation (RAG)</b> 📚 using Gemini Flash
          model to try building a chatbot that can answer question based on the
          uploaded documents.
        </div>
        <div className="space-y-6">
          <ApiKeyInput onApiKeyChange={handleApiKeyChange} />
          {hasApiKey ? (
            <>
              <div
                className="rounded-lg bg-red-50 p-4 text-sm text-red-800 dark:bg-gray-800 dark:text-red-400"
                role="alert"
              >
                <span className="font-medium">Important!</span> For now I only
                support PDF files.
              </div>
              <FileUpload />
              <Chat />
            </>
          ) : (
            <div className="rounded-lg bg-yellow-50 p-4 text-sm text-yellow-800 dark:bg-gray-800 dark:text-yellow-400">
              Please enter your Gemini API key to use the application.
            </div>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
