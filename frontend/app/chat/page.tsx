// frontend/app/chat/page.tsx
'use client';

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function ChatPage() {
  const [message, setMessage] = useState('');
  const [answer, setAnswer] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    setIsLoading(true);
    setAnswer(null);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          history: [],
        }),
      });

      const data = await res.json();
      setAnswer(data.answer ?? '');
    } catch (err) {
      console.error(err);
      setAnswer(
        'Sorry, something went wrong while contacting the StreamIntel360 backend.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main>
      {/* Header */}
      <header
        style={{
          marginBottom: '1.75rem',
        }}
      >
        <h1
          style={{
            fontSize: '2.25rem',
            fontWeight: 800,
            margin: 0,
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            color: '#4c1d95', // purple
          }}
        >
          <span aria-hidden="true" style={{ fontSize: '2.1rem' }}>
            🎬
          </span>
          <span>StreamIntel360 – Content Intelligence Copilot</span>
        </h1>
        <p
          style={{
            marginTop: '0.9rem',
            marginBottom: '0.35rem',
            fontSize: '1rem',
            lineHeight: 1.6,
            maxWidth: '52rem',
          }}
        >
          Describe a show or movie concept, and the AI agents will analyze it
          from multiple angles (similar content, audience fit, competitive
          space) and produce an executive-style summary.
        </p>
        <p
          style={{
            margin: 0,
            fontSize: '0.98rem',
            color: '#4b5563',
          }}
        >
          Start by describing a concept or question about a show or movie.
        </p>
      </header>

      {/* Input section (kept constant at the top) */}
      <section
        aria-label="Concept input"
        style={{
          marginBottom: '2rem',
        }}
      >
        <form onSubmit={handleSubmit}>
          <label
            htmlFor="concept"
            style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: 600,
            }}
          >
            Show / movie concept or question
          </label>
          <div
            style={{
              display: 'flex',
              alignItems: 'stretch',
              gap: '0.75rem',
            }}
          >
            <textarea
              id="concept"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Describe your show/movie concept or ask a question..."
              rows={3}
              style={{
                flex: 1,
                resize: 'vertical',
                padding: '0.9rem 1rem',
                borderRadius: '0.75rem',
                border: '1px solid #d1d5db',
                fontSize: '0.98rem',
                lineHeight: 1.5,
                outline: 'none',
              }}
            />
            <button
              type="submit"
              disabled={isLoading}
              style={{
                minWidth: '96px',
                borderRadius: '0.75rem',
                border: 'none',
                padding: '0 1.2rem',
                fontSize: '1rem',
                fontWeight: 600,
                backgroundColor: isLoading ? '#9ca3af' : '#020617',
                color: '#ffffff',
                cursor: isLoading ? 'default' : 'pointer',
                alignSelf: 'flex-end',
                height: '3rem',
              }}
            >
              {isLoading ? 'Thinking…' : 'Send'}
            </button>
          </div>
        </form>
      </section>

      {/* Answer section (always below fields) */}
      {answer && (
        <section
          aria-label="AI analysis"
          style={{
            marginTop: '0.5rem',
            borderTop: '1px solid #e5e7eb',
            paddingTop: '1.25rem',
          }}
        >
          <h2
            style={{
              fontSize: '1.1rem',
              fontWeight: 700,
              marginBottom: '0.75rem',
            }}
          >
            AI Strategy View:
          </h2>
          <div
            style={{
              fontSize: '0.98rem',
              lineHeight: 1.7,
            }}
          >
            <ReactMarkdown>{answer}</ReactMarkdown>
          </div>
        </section>
      )}
    </main>
  );
}