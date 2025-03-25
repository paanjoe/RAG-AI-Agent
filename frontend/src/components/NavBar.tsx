'use client';

import { Button } from 'flowbite-react';

import { useState } from 'react';

import TechnicalDiagram from '@/components/TechnicalDiagram';
import { useTheme } from '@/components/ThemeProvider';

export default function Navbar() {
  const { theme, toggleTheme } = useTheme();
  const [showDiagram, setShowDiagram] = useState(false);

  return (
    <>
      <nav className="border-b bg-white px-4 py-3 dark:border-gray-800 dark:bg-gray-900">
        <div className="container mx-auto flex max-w-4xl items-center justify-between">
          <h1 className="text-xl font-bold text-gray-900 dark:text-white">
            RAG AI Assistant
          </h1>
          <div className="flex items-center gap-2">
            <Button
              color="gray"
              size="sm"
              onClick={() => setShowDiagram(true)}
              className="flex items-center gap-1"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="h-5 w-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z"
                />
              </svg>
              Technical Diagram
            </Button>
            <Button
              onClick={toggleTheme}
              color="gray"
              size="sm"
              className="p-2"
            >
              {theme === 'light' ? (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="h-5 w-5"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z"
                  />
                </svg>
              ) : (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="h-5 w-5"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z"
                  />
                </svg>
              )}
            </Button>
          </div>
        </div>
      </nav>
      <TechnicalDiagram
        isOpen={showDiagram}
        onClose={() => setShowDiagram(false)}
      />
    </>
  );
}
