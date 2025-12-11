// frontend/app/analyze/page.tsx
'use client';

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function AnalyzePage() {
  const [titleName, setTitleName] = useState('Time Loop Colony');
  const [description, setDescription] = useState('');
  const [regions, setRegions] = useState('US');
  const [answer, setAnswer] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();

    setIsLoading(true);
    setAnswer(null);

    try {
      const body = {
        title_name: titleName,
        description: description || undefined,
        target_regions: regions
          ? regions
              .split(',')
              .map((r) => r.trim())
              .filter(Boolean)
          : undefined,
      };

      const res = await fetch('http://127.0.0.1:8000/api/analyze_title', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
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
            🎯
          </span>
          <span>Analyze a Show or Movie Concept</span>
        </h1>
        <p
          style={{
            marginTop: '0.9rem',
            marginBottom: 0,
            fontSize: '1rem',
            lineHeight: 1.6,
            maxWidth: '52rem',
          }}
        >
          Enter a working title, a short synopsis, and (optionally) a few
          target regions. StreamIntel360 will pull similar titles from the
          catalog and generate an executive-style strategy summary.
        </p>
      </header>

      {/* Form section (fields stay fixed at the top) */}
      <section
        aria-label="Title analysis form"
        style={{ marginBottom: '2rem' }}
      >
        <form onSubmit={handleAnalyze}>
          <div style={{ marginBottom: '1rem' }}>
            <label
              htmlFor="titleName"
              style={{ display: 'block', fontWeight: 600, marginBottom: '0.35rem' }}
            >
              Title Name
            </label>
            <input
              id="titleName"
              type="text"
              value={titleName}
              onChange={(e) => setTitleName(e.target.value)}
              style={{
                width: '100%',
                padding: '0.7rem 0.85rem',
                borderRadius: '0.75rem',
                border: '1px solid #d1d5db',
                fontSize: '0.98rem',
              }}
            />
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label
              htmlFor="description"
              style={{ display: 'block', fontWeight: 600, marginBottom: '0.35rem' }}
            >
              Description (optional)
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Short synopsis of the concept..."
              rows={4}
              style={{
                width: '100%',
                padding: '0.9rem 1rem',
                borderRadius: '0.75rem',
                border: '1px solid #d1d5db',
                fontSize: '0.98rem',
                resize: 'vertical',
              }}
            />
          </div>

          <div style={{ marginBottom: '1.25rem' }}>
            <label
              htmlFor="regions"
              style={{ display: 'block', fontWeight: 600, marginBottom: '0.35rem' }}
            >
              Target Regions (optional, comma-separated)
            </label>
            <input
              id="regions"
              type="text"
              value={regions}
              onChange={(e) => setRegions(e.target.value)}
              style={{
                width: '100%',
                padding: '0.7rem 0.85rem',
                borderRadius: '0.75rem',
                border: '1px solid #d1d5db',
                fontSize: '0.98rem',
              }}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            style={{
              borderRadius: '0.75rem',
              border: 'none',
              padding: '0.65rem 1.4rem',
              fontSize: '1rem',
              fontWeight: 600,
              backgroundColor: isLoading ? '#9ca3af' : '#020617',
              color: '#ffffff',
              cursor: isLoading ? 'default' : 'pointer',
            }}
          >
            {isLoading ? 'Analyzing…' : 'Run Analysis'}
          </button>
        </form>
      </section>

      {/* Answer section (below the form) */}
      {answer && (
        <section
          aria-label="Title analysis results"
          style={{
            marginTop: '0.5rem',
            borderTop: '1px solid #e5e7eb',
            paddingTop: '1.25rem',
          }}
        >
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