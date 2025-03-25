'use client';

import { useState } from 'react';
import api from '@/lib/api';

type Message = {
  text: string;
  isUser: boolean;
};

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    try {
      setMessages(prev => [...prev, { text: input, isUser: true }]);
      setInput('');
      
      const response = await api.post('/chat', {
        question: input
      });
      
      setMessages(prev => [...prev, { text: response.data.response, isUser: false }]);
    } catch (error: any) {
      console.error('Chat error:', error);
      // Show error message to user
      setMessages(prev => [...prev, { 
        text: error.response?.data?.detail || 'An error occurred. Please try uploading the PDF again.',
        isUser: false
      }]);
    }
  };

  return (
    <div className="w-full max-w-2xl p-4 border rounded-lg">
      <div className="h-[400px] overflow-y-auto mb-4">
        {messages.map((message, i) => (
          <div
            key={i}
            className={`p-2 mb-2 rounded ${
              message.isUser ? 'bg-blue-100 ml-auto text-black' : 'bg-gray-100 text-black'
            } max-w-[80%]`}
          >
            {message.text}
          </div>
        ))}
        {loading && <div className="text-gray-500">Loading...</div>}
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 p-2 border rounded"
          placeholder="Ask a question..."
        />
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-blue-300"
        >
          Send
        </button>
      </form>
    </div>
  );
}