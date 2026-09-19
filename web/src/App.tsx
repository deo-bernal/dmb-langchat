import { useEffect, useMemo, useRef, useState } from "react";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import type { Id } from "../../convex/_generated/dataModel";
import { getSessionId } from "./session";

const API_URL = (import.meta.env.VITE_API_URL as string) || "http://localhost:8080";

export default function App() {
  const sessionId = useMemo(() => getSessionId(), []);
  const threads = useQuery(api.threads.listBySession, { sessionId });
  const createThread = useMutation(api.threads.create);

  const [threadId, setThreadId] = useState<Id<"threads"> | null>(null);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const messages = useQuery(
    api.messages.listByThread,
    threadId ? { threadId } : "skip"
  );

  useEffect(() => {
    if (!threadId && threads && threads.length > 0) {
      setThreadId(threads[0]._id);
    }
  }, [threads, threadId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, busy]);

  async function onNewChat() {
    setError(null);
    const id = await createThread({ sessionId, title: "New chat" });
    setThreadId(id);
  }

  async function onSend() {
    const text = draft.trim();
    if (!text || busy) return;
    setBusy(true);
    setError(null);
    setDraft("");
    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId,
          threadId: threadId ?? undefined,
          message: text,
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data.detail || `Chat failed (${res.status})`);
      }
      if (data.threadId && data.threadId !== threadId) {
        setThreadId(data.threadId as Id<"threads">);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
      setDraft(text);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          DMB LangChat
          <span>LangChain memory on Convex</span>
        </div>
        <button className="btn" type="button" onClick={onNewChat}>
          New chat
        </button>
        <ul className="thread-list">
          {(threads ?? []).map((t) => (
            <li key={t._id}>
              <button
                type="button"
                className={t._id === threadId ? "active" : ""}
                onClick={() => setThreadId(t._id)}
              >
                {t.title}
              </button>
            </li>
          ))}
        </ul>
        <button
          className="btn ghost"
          type="button"
          onClick={() => window.open("https://www.dmbwebsolutions.com", "_blank")}
        >
          DMB Web Solutions
        </button>
      </aside>

      <main className="main">
        <header>
          <h1>{threads?.find((t) => t._id === threadId)?.title || "Conversation"}</h1>
          <p>
            Messages persist in Convex. Refresh the page — your thread is still here.
          </p>
        </header>

        <div className="messages">
          {!threadId && (
            <div className="empty">
              <strong>Start a thread</strong>
              Ask anything. History is stored permanently (unlike the lab RAM list).
            </div>
          )}
          {(messages ?? []).map((m) => (
            <div key={m._id} className={`bubble ${m.role === "human" ? "human" : "ai"}`}>
              {m.content}
            </div>
          ))}
          {busy && <div className="bubble ai">Thinking…</div>}
          <div ref={bottomRef} />
        </div>

        {error ? <div className="error">{error}</div> : null}

        <div className="composer">
          <textarea
            value={draft}
            placeholder="Message LangChat…"
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                void onSend();
              }
            }}
          />
          <button className="btn" type="button" disabled={busy || !draft.trim()} onClick={() => void onSend()}>
            Send
          </button>
        </div>
      </main>
    </div>
  );
}
