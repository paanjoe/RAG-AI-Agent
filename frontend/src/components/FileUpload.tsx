'use client';

import { useState } from 'react';
import { uploadPDF } from '@/lib/api';

export default function FileUpload() {
  const [uploading, setUploading] = useState(false);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;
    
    setUploading(true);
    try {
      await uploadPDF(e.target.files[0]);
      alert('PDF uploaded and processed successfully!');
    } catch (error) {
      console.error(error);
      alert('Error uploading PDF');
    } finally {
      setUploading(false);
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