'use client';

import { Button, TextInput } from 'flowbite-react';

import { useEffect, useState } from 'react';

interface ApiKeyInputProps {
  onApiKeyChange: (apiKey: string | null) => void;
}

export default function ApiKeyInput({ onApiKeyChange }: ApiKeyInputProps) {
  const [apiKey, setApiKey] = useState<string>('');
  const [isEditing, setIsEditing] = useState<boolean>(true);

  // Check for existing API key in localStorage on component mount
  useEffect(() => {
    const savedApiKey = localStorage.getItem('gemini_api_key');
    if (savedApiKey) {
      setApiKey(savedApiKey);
      setIsEditing(false);
      onApiKeyChange(savedApiKey);
    }
  }, [onApiKeyChange]);

  const handleSave = () => {
    if (apiKey.trim()) {
      localStorage.setItem('gemini_api_key', apiKey);
      setIsEditing(false);
      onApiKeyChange(apiKey);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    onApiKeyChange(null);
  };

  const handleClear = () => {
    setApiKey('');
    setIsEditing(true);
    localStorage.removeItem('gemini_api_key');
    onApiKeyChange(null);
  };

  return (
    <div className="w-full rounded-lg bg-white p-6 shadow-lg dark:bg-gray-800">
      <div className="space-y-4">
        <div className="flex flex-col space-y-2">
          <label className="text-sm font-medium text-gray-900 dark:text-white">
            Google (Gemini) API Key
          </label>
          {isEditing ? (
            <div className="flex gap-2">
              <TextInput
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Enter your Gemini API key"
                className="flex-1"
              />
              <Button onClick={handleSave} disabled={!apiKey.trim()}>
                Save
              </Button>
            </div>
          ) : (
            <div className="flex gap-2">
              <div className="flex-1 rounded-lg bg-gray-100 px-4 py-2 dark:bg-gray-700">
                <span className="text-gray-800 dark:text-gray-200">
                  API Key: ••••••••{apiKey.slice(-4)}
                </span>
              </div>
              <Button color="gray" onClick={handleEdit}>
                Edit
              </Button>
              <Button color="failure" onClick={handleClear}>
                Clear
              </Button>
            </div>
          )}
        </div>
        <div className="text-sm text-gray-600 dark:text-gray-400">
          <p>
            Your API key is stored locally in your browser and will be deleted
            when you clear your browser data or click the Clear button.
          </p>
          <p className="mt-2">
            Don&apos;t have an API key?{' '}
            <a
              href="https://makersuite.google.com/app/apikey"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline dark:text-blue-400"
            >
              Get one here
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
