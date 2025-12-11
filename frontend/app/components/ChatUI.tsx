"use client";

import { useState } from "react";

type Message = {
  role: "user" | "ai";
  content: string;
};

type ChatResponse = {
  session_id: string;
  answer: string;
  sources: any[];
};

export default function ChatUI() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!input.trim()) return;

    const userMsg: Message = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMsg.content,
          // simple history: all previous message texts
          history: messages.map((m) => m.content),
        }),
      });

      if (!res.ok) {
        throw new Error(`Backend error: ${res.status}`);
      }

      const data: ChatResponse = await res.json();

      const aiMsg: Message = {
        role: "ai",
        content: data.answer || "No answer returned from backend.",
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
      const aiMsg: Message = {
        role: "ai",
        content:
          "Sorry, something went wrong while calling the backend. Please check the backend logs and try again.",
      };
      setMessages((prev) => [...prev, aiMsg]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-3xl mx-auto py-8">
      <div className="border rounded-md p-4 mb-4 h-80 overflow-y-auto bg-black/5">
        {messages.length === 0 && (
          <p className="text-gray-500">
            Start by describing a concept or question about a show/movie.
          </p>
        )}
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`mb-2 ${
              m.role === "user" ? "text-blue-600" : "text-green-700"
            }`}
          >
            <strong>{m.role === "user" ? "You:" : "AI:"}</strong>{" "}
            <span className="whitespace-pre-wrap">{m.content}</span>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <textarea
          className="flex-1 border rounded-md p-2"
          rows={3}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your show/movie concept or ask a question..."
        />
        <button
          onClick={send}
          disabled={loading}
          className="px-4 py-2 bg-red-600 text-white rounded-md disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>
    </div>
  );
}