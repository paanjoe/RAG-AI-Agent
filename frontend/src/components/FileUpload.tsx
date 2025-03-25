'use client';

import { useState } from 'react';
import api from '@/lib/api';

export default function FileUpload() {
  const [uploading] = useState(false);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      // Handle successful upload
      console.log('Upload successful:', response.data);
    } catch (error) {
      console.error('Upload failed:', error);
      // Handle error
    }
  };

  return (
    <div className="w-full max-w-md p-4 border rounded-lg">
      <label className="block mb-2 text-sm font-medium">
        Upload PDF
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileUpload}
          disabled={uploading}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
        />
      </label>
      {uploading && <p>Processing...</p>}
    </div>
  );
}