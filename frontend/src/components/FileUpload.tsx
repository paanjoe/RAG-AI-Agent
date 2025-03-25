'use client';

import { Button } from 'flowbite-react';

import { useState } from 'react';

import api from '@/lib/api';

export default function FileUpload() {
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="w-full rounded-lg bg-white p-6 shadow-lg dark:bg-gray-800">
      <div className="flex items-center gap-4">
        <Button disabled={uploading} color="gray">
          <label className="cursor-pointer">
            {uploading ? 'Uploading...' : 'Choose File'}
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>
        </Button>
        {fileName && (
          <span className="text-sm text-gray-600 dark:text-gray-300">
            Selected file: {fileName}
          </span>
        )}
      </div>
    </div>
  );
}
