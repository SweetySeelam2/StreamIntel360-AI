// frontend/app/page.tsx
import Link from "next/link";

export default function HomePage() {
  return (
    <main
      style={{
        maxWidth: "960px",
        margin: "2.5rem auto",
        padding: "0 1.25rem",
        fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        lineHeight: 1.6,
      }}
    >
      <header style={{ marginBottom: "2rem" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "0.5rem" }}>🎬 StreamIntel360</h1>
        <p style={{ fontSize: "1.1rem", margin: 0 }}>
          Multi-Agent Content Intelligence Platform for Streaming Strategy.
        </p>
      </header>

      <section style={{ marginBottom: "1.75rem" }}>
        <p>
          StreamIntel360 helps streaming teams evaluate new show and movie concepts using AI agents powered by
          Retrieval-Augmented Generation (RAG), LangGraph, and large language models.
        </p>
        <ul style={{ paddingLeft: "1.5rem" }}>
          <li>Analyze a concept&apos;s audience fit and competitive landscape.</li>
          <li>Discover similar titles and patterns from the existing catalog.</li>
          <li>Generate executive-ready summaries for Go / No-Go decisions.</li>
        </ul>
      </section>

      <section style={{ marginTop: "2rem", fontSize: "1.05rem" }}>
        <span>Try one of the tools:</span>
        <div style={{ marginTop: "0.75rem" }}>
          <Link
            href="/chat"
            style={{
              marginRight: "1.5rem",
              textDecoration: "underline",
            }}
          >
            Try AI Copilot
          </Link>
          <Link
            href="/analyze"
            style={{
              textDecoration: "underline",
            }}
          >
            Analyze a Title
          </Link>
        </div>
      </section>
    </main>
  );
}