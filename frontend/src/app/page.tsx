import FileUpload from '@/components/FileUpload';
import Chat from '@/components/Chat';

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold text-center">RAG AI Assistant</h1>
        <FileUpload />
        <Chat />
      </div>
    </main>
  );
}